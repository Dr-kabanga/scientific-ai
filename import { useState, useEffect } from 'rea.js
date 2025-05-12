import { useState, useEffect } from 'react';
import { Card, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Avatar } from "@/components/ui/avatar";
import { Badge } from "@/components/ui/badge";
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer } from 'recharts';
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class WorkforceCreate(BaseModel):
    nrc: str
    name: str
    employer: str
    zra_income_sources: int
    last_worklog_submitted: Optional[datetime]
    productivity_index: Optional[float]
    circular_compliance_score: Optional[float]

class WorkforceResponse(WorkforceCreate):
    id: int

    class Config:
        orm_mode = True

export default function ZRAWorkforceDashboard() {
  const [loading, setLoading] = useState(true);
  const [profile, setProfile] = useState(null);
  const [workforceData, setWorkforceData] = useState([]);

  useEffect(() => {
    // Fetch workforce data from the backend
    fetch("http://localhost:8000/workforce")
      .then((response) => {
        if (!response.ok) {
          throw new Error("Failed to fetch workforce data");
        }
        return response.json();
      })
      .then((data) => {
        setWorkforceData(data);
        setLoading(false);
      })
      .catch((error) => {
        console.error("Error fetching workforce data:", error);
        setLoading(false);forceData.length === 0) {
      });lable.</p>;
  }, []);

  const handleSubmitWorklog = () => {
    const newWorklog = {
      nrc: "123456789",
      name: "John Doe",
      employer: "Ministry of Health",
      zra_income_sources: 2,
      last_worklog_submitted: new Date().toISOString(),
      productivity_index: 85.5,
      circular_compliance_score: 90.2,
    };

    fetch("http://localhost:8000/workforce", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(newWorklog),
    })
      .then((response) => response.json())
      .then((data) => {
        console.log("Worklog submitted:", data);
      })
      .catch((error) => console.error("Error submitting worklog:", error));
  };

  if (loading) {
    return <p>Loading...</p>;
  }rce Compliance Dashboard</h1>

  return (
    <div className="p-6 grid gap-4">me="p-4 flex items-center justify-between">
      <h1 className="text-2xl font-bold">ZRA Workforce Compliance Dashboard</h1>assName="flex items-center gap-4">

      {profile && (
        <Card className="p-4 flex items-center justify-between">
          <div className="flex items-center gap-4">
            <Avatar> className="text-lg font-semibold">{profile.name}</p>
              <img src="/biometric_placeholder.png" alt="Biometric ID" />ile.NRC}</p>
            </Avatar>Badge variant="outline">Compliance: {profile.compliance}</Badge>
            <div>    </div>
              <p className="text-lg font-semibold">{profile.name}</p>          </div>
              <p className="text-sm text-gray-600">NRC: {profile.NRC}</p>utton variant="secondary" onClick={handleSubmitWorklog}>
  Submit Worklog
</Button>
              <Badge variant="outline">Compliance: {profile.compliance}</Badge>
            </div>
          </div>
          <Button variant="secondary">Submit Worklog</Button>
        </Card>
      )}="text-xl font-bold mb-2">Ministry Compliance Overview</h2>
ainer width="100%" height={300}>
      <Card>
        <CardContent>taKey="name" />
          <h2 className="text-xl font-bold mb-2">Ministry Compliance Overview</h2>
          <ResponsiveContainer width="100%" height={300}> />
            <BarChart data={workforceData}> <Bar dataKey="compliance" fill="#10B981" />
              <XAxis dataKey="name" />            </BarChart>
              <YAxis />ner>
              <Tooltip />
              <Bar dataKey="compliance" fill="#10B981" />
            </BarChart>
          </ResponsiveContainer>lassName="p-4">
        </CardContent>2 className="text-xl font-semibold mb-2">Biometric Login Panel</h2>
      </Card>    <Input placeholder="Scan NRC Thumbprint or Enter NRC Manually..." />
       <Button className="mt-2">Authenticate</Button>
      <Card className="p-4">      </Card>
        <h2 className="text-xl font-semibold mb-2">Biometric Login Panel</h2>
        <Input placeholder="Scan NRC Thumbprint or Enter NRC Manually..." />  );
        <Button className="mt-2">Authenticate</Button>
      </Card>
    </div>
  );
}

from fastapi.middleware.cors import CORSMiddleware   allow_origins=["http://localhost:3000"],  # React frontend URL

from app.database import Base, engine
from app.models.workforce import Workforce

Base.metadata.create_all(bind=engine)    allow_headers=["*"],    allow_methods=["*"],    allow_credentials=True,    allow_origins=["http://localhost:3000"],  # React frontend URL    CORSMiddleware,app.add_middleware(    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
))    allow_headers=["*"],    allow_methods=["*"],    allow_credentials=True,    allow_origins=["http://localhost:3000"],  # React frontend URL    CORSMiddleware,app.add_middleware(    allow_credentials=True,    allow_methods=["*"],    allow_headers=["*"],)

CREATE TABLE workforce (
    id SERIAL PRIMARY KEY,
    nrc VARCHAR(255) UNIQUE NOT NULL,
    name VARCHAR(255) NOT NULL,
    employer VARCHAR(255),
    zra_income_sources INT,
    last_worklog_submitted TIMESTAMP,
    productivity_index FLOAT,
    circular_compliance_score FLOAT
);