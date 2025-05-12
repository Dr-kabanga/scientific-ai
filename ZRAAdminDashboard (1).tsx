import React, { useState, useEffect } from 'react';
import { Card, CardContent } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Table, TableHead, TableRow, TableCell, TableBody } from '@/components/ui/table';
import { Input } from '@/components/ui/input';
import { BadgeCheck, AlertTriangle } from 'lucide-react';
import axios from 'axios';
import { toast } from 'react-toastify'; // Error notification
import 'react-toastify/dist/ReactToastify.css'; // Toastify CSS
import Spinner from '@/components/ui/spinner'; // Loading spinner component

// Set global API key from environment variable
axios.defaults.headers.common['x-api-key'] = process.env.REACT_APP_API_KEY || '';

const ZRAAdminDashboard = () => {
  const [attendanceData, setAttendanceData] = useState([]);
  const [dualIncomeData, setDualIncomeData] = useState([]);
  const [search, setSearch] = useState('');
  const [loading, setLoading] = useState({ attendance: false, dualIncome: false });

  useEffect(() => {
    fetchAttendance();
    fetchDualIncome();
  }, []);

  const fetchAttendance = async () => {
    setLoading((prev) => ({ ...prev, attendance: true }));
    try {
      const res = await axios.get('/api/attendance');
      setAttendanceData(res.data);
    } catch (err) {
      console.error('Attendance fetch failed:', err);
      toast.error('Failed to fetch attendance data.');
    } finally {
      setLoading((prev) => ({ ...prev, attendance: false }));
    }
  };

  const fetchDualIncome = async () => {
    setLoading((prev) => ({ ...prev, dualIncome: true }));
    try {
      const res = await axios.get('/api/dual_income');
      setDualIncomeData(res.data);
    } catch (err) {
      console.error('Dual income fetch failed:', err);
      toast.error('Failed to fetch dual income data.');
    } finally {
      setLoading((prev) => ({ ...prev, dualIncome: false }));
    }
  };

  const filteredAttendance = attendanceData.filter((record) =>
    record.name.toLowerCase().includes(search.toLowerCase())
  );

  return (
    <div className="p-6 space-y-8">
      <h1 className="text-3xl font-bold">ZRA Cabinet Enforcement Dashboard</h1>

      <div className="space-y-4">
        <Card>
          <CardContent className="p-4">
            <h2 className="text-xl font-semibold mb-2">Biometric Attendance Summary</h2>
            <Input
              placeholder="Search employee..."
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              className="mb-4"
              aria-label="Search employee by name"
            />
            {loading.attendance ? (
              <Spinner /> // Display spinner while loading
            ) : (
              <Table>
                <TableHead>
                  <TableRow>
                    <TableCell>Name</TableCell>
                    <TableCell>Role</TableCell>
                    <TableCell>Hours Worked</TableCell>
                    <TableCell>Required Hours</TableCell>
                    <TableCell>Status</TableCell>
                  </TableRow>
                </TableHead>
                <TableBody>
                  {filteredAttendance.map((person) => (
                    <TableRow key={person.id}>
                      <TableCell>{person.name}</TableCell>
                      <TableCell>{person.role}</TableCell>
                      <TableCell>{person.hours}</TableCell>
                      <TableCell>{person.required}</TableCell>
                      <TableCell>
                        {person.hours >= person.required ? (
                          <BadgeCheck className="text-green-600" aria-label="Status: On track" />
                        ) : (
                          <AlertTriangle className="text-red-600" aria-label="Status: Off track" />
                        )}
                      </TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            )}
          </CardContent>
        </Card>

        <Card>
          <CardContent className="p-4">
            <h2 className="text-xl font-semibold mb-2">Dual Income Detection</h2>
            {loading.dualIncome ? (
              <Spinner /> // Display spinner while loading
            ) : (
              <Table>
                <TableHead>
                  <TableRow>
                    <TableCell>Name</TableCell>
                    <TableCell>Gov Payslip (ZMW)</TableCell>
                    <TableCell>Private Income (ZMW)</TableCell>
                    <TableCell>Discrepancy</TableCell>
                  </TableRow>
                </TableHead>
                <TableBody>
                  {dualIncomeData.map((person) => (
                    <TableRow key={person.id}>
                      <TableCell>{person.name}</TableCell>
                      <TableCell>{person.govPay}</TableCell>
                      <TableCell>{person.privatePay}</TableCell>
                      <TableCell>
                        {person.flag === 'YES' ? (
                          <AlertTriangle className="text-red-600" aria-label="Discrepancy detected" />
                        ) : (
                          <BadgeCheck className="text-green-600" aria-label="No discrepancy" />
                        )}
                      </TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            )}
          </CardContent>
        </Card>
      </div>

      <div className="flex justify-end">
        <Button onClick={() => window.print()} aria-label="Export report">
          Export Report
        </Button>
      </div>
    </div>
  );
};

export default ZRAAdminDashboard;