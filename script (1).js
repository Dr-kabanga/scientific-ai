function showTime() {
	document.getElementById('currentTime').innerHTML = new Date().toUTCString();
}
showTime();
setInterval(function () {
	showTime();
}, 1000);
npm install express speakeasy qrcode body-parser jsonwebtoken
// models/user.js
const users = {}; // { email: { passwordHash, totpSecret, provisionalSecret } }
module.exports = users;
const express = require('express');
const bodyParser = require('body-parser');
const speakeasy = require('speakeasy');
const qrcode = require('qrcode');
const jwt = require('jsonwebtoken');
const users = require('./models/user');

const app = express();
app.use(bodyParser.json());

const JWT_SECRET = 'replace_with_strong_secret';
const AUTH_TOKEN_EXPIRY = '1h';

// 1. TOTP Setup: generate secret + QR
app.post('/api/mfa/setup', (req, res) => {
  const { email } = req.body;
  if (!users[email]) return res.status(404).json({ error: 'User not found' });

  const secret = speakeasy.generateSecret({ length: 20, name: `USAFiO (${email})` });
  users[email].provisionalSecret = secret.base32;

  qrcode.toDataURL(secret.otpauth_url, (err, url) => {
    if (err) return res.status(500).json({ error: 'QR generation failed' });
    res.json({ qr: url, secret: secret.base32 });
  });
});

// 2. Verify Setup: user enters first TOTP code
app.post('/api/mfa/verify-setup', (req, res) => {
  const { email, token } = req.body;
  const user = users[email];
  const { provisionalSecret } = user || {};
  const verified = speakeasy.totp.verify({
    secret: provisionalSecret,
    encoding: 'base32',
    token,
    window: 1
  });

  if (verified) {
    user.totpSecret = provisionalSecret;
    delete user.provisionalSecret;
    return res.json({ success: true });
  }
  res.status(400).json({ error: 'Invalid token' });
});

// 3. Login + TOTP check
app.post('/api/login', (req, res) => {
  const { email, password } = req.body;
  const user = users[email];
  // TODO: verify password hash
  if (!user || password !== user.passwordHash) {
    return res.status(401).json({ error: 'Invalid credentials' });
  }
  if (user.totpSecret) {
    // Tell client MFA step is required
    return res.json({ mfaRequired: true });
  }
  const token = jwt.sign({ email }, JWT_SECRET, { expiresIn: AUTH_TOKEN_EXPIRY });
  res.json({ token });
});

// 4. Verify TOTP and issue JWT
app.post('/api/mfa/verify', (req, res) => {
  const { email, token: totpToken } = req.body;
  const user = users[email];
  const valid = speakeasy.totp.verify({
    secret: user.totpSecret,
    encoding: 'base32',
    token: totpToken,
    window: 1
  });
  if (!valid) return res.status(400).json({ error: 'Invalid TOTP' });
  const authToken = jwt.sign({ email }, JWT_SECRET, { expiresIn: AUTH_TOKEN_EXPIRY });
  res.json({ token: authToken });
});

app.listen(3000, () => console.log('TOTP MFA server listening on :3000'));
npm install express @simplewebauthn/server cookie-parser body-parser express-session
const express = require('express');
const session = require('express-session');
const { 
  generateRegistrationOptions,
  verifyAttestationResponse,
  generateAuthenticationOptions,
  verifyAssertionResponse,
} = require('@simplewebauthn/server');

const app = express();
app.use(express.json());
app.use(session({ secret: 'replace_with_strong', resave: false, saveUninitialized: true }));

// In-memory store for demo
const users = {}; 
// rp (Relying Party) config
const rpID = 'your.domain.com';
const origin = 'https://your.domain.com';

app.get('/webauthn/register-options', (req, res) => {
  const { email } = req.query;
  if (!users[email]) users[email] = { credentials: [] };
  const user = users[email];

  const options = generateRegistrationOptions({
    rpName: 'USAFiO',
    rpID,
    userID: email,
    userName: email,
    attestationType: 'indirect',
    authenticatorSelection: {
      userVerification: 'preferred',
      requireResidentKey: false,
    },
    excludeCredentials: user.credentials.map(cred => ({
      id: Buffer.from(cred.credentialID, 'base64url'),
      type: 'public-key',
    })),
  });

  req.session.challenge = options.challenge;
  res.json(options);
});

app.post('/webauthn/register-verify', async (req, res) => {
  const { email, attestationResponse } = req.body;
  const expectedChallenge = req.session.challenge;
  try {
    const verification = await verifyAttestationResponse({
      response: attestationResponse,
      expectedChallenge,
      expectedOrigin: origin,
      expectedRPID: rpID,
    });

    const { verified, registrationInfo } = verification;
    if (verified && registrationInfo) {
      const { credentialPublicKey, credentialID, counter } = registrationInfo;
      users[email].credentials.push({
        credentialID: credentialID.toString('base64url'),
        publicKey: credentialPublicKey,
        counter,
      });
    }
    res.json({ verified });
  } catch (error) {
    res.status(400).json({ error: error.message });
  }
});

app.get('/webauthn/authn-options', (req, res) => {
  const { email } = req.query;
  const user = users[email];
  if (!user) return res.status(404).json({ error: 'Not registered' });

  const options = generateAuthenticationOptions({
    allowCredentials: user.credentials.map(cred => ({
      id: Buffer.from(cred.credentialID, 'base64url'),
      type: 'public-key',
    })),
    userVerification: 'preferred',
    rpID,
  });

  req.session.challenge = options.challenge;
  res.json(options);
});

app.post('/webauthn/authn-verify', async (req, res) => {
  const { email, assertionResponse } = req.body;
  const expectedChallenge = req.session.challenge;
  const user = users[email];
  try {
    const verification = await verifyAssertionResponse({
      response: assertionResponse,
      expectedChallenge,
      expectedOrigin: origin,
      expectedRPID: rpID,
      authenticator: user.credentials.find(c => c.credentialID === assertionResponse.id),
    });

    if (verification.verified) {
      // Update counter to prevent replay
      user.credentials.find(c => c.credentialID === assertionResponse.id).counter = verification.authenticationInfo.newCounter;
      res.json({ verified: true });
    } else {
      res.status(401).json({ verified: false });
    }
  } catch (error) {
    res.status(400).json({ error: error.message });
  }
});

app.listen(3001, () => console.log('WebAuthn server on :3001'));
import { startRegistration } from '@simplewebauthn/browser';

async function register(email) {
  const opts = await fetch(`/webauthn/register-options?email=${email}`).then(r => r.json());
  const attResp = await startRegistration(opts);
  await fetch('/webauthn/register-verify', {
    method: 'POST',
    headers: {'Content-Type':'application/json'},
    body: JSON.stringify({ email, attestationResponse: attResp })
  });
}
import { startAuthentication } from '@simplewebauthn/browser';

async function authenticate(email) {
  const opts = await fetch(`/webauthn/authn-options?email=${email}`).then(r => r.json());
  const authResp = await startAuthentication(opts);
  const { verified } = await fetch('/webauthn/authn-verify', {
    method: 'POST',
    headers: {'Content-Type':'application/json'},
    body: JSON.stringify({ email, assertionResponse: authResp })
  }).then(r => r.json());
  if (verified) console.log('Logged in via WebAuthn!');
}
