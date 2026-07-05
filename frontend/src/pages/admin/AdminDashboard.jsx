import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Link } from 'react-router-dom';
import { BarChart3, Download, Users, BookOpen, UserCheck, GraduationCap } from 'lucide-react';

export default function AdminDashboard() {
  const [report, setReport] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchAnalytics = async () => {
      try {
        const res = await axios.get('/api/v1/protected/analytics/reports');
        setReport(res.data.data);
      } catch (err) {
        console.error(err);
      } finally {
        setLoading(false);
      }
    };
    fetchAnalytics();
  }, []);

  const triggerExport = async () => {
    try {
      const res = await axios.post('/api/v1/protected/analytics/export');
      alert(res.data.message);
    } catch (err) {
      alert("Gagal memicu ekspor CSV.");
    }
  };

  if (loading) {
    return (
      <div className="flex justify-center py-20">
        <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-slate-800"></div>
      </div>
    );
  }

  return (
    <div className="space-y-8">
      <div className="flex flex-col md:flex-row justify-between items-start md:items-center bg-white p-8 rounded-3xl shadow-sm border border-slate-100 gap-4">
        <div>
          <h1 className="text-3xl font-extrabold text-slate-900 mb-2">Admin Analytics</h1>
          <p className="text-slate-500">Pantau performa platform LMS secara keseluruhan.</p>
        </div>
        <button 
          onClick={triggerExport}
          className="flex items-center space-x-2 bg-slate-800 hover:bg-slate-900 text-white px-6 py-3 rounded-xl font-semibold transition-colors shadow-md"
        >
          <Download className="w-5 h-5" />
          <span>Export CSV Report</span>
        </button>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <Link to="/admin/users" className="bg-white p-6 rounded-2xl shadow-sm border border-slate-100 flex items-center space-x-4 hover:border-apple-blue transition-colors cursor-pointer group">
          <div className="bg-blue-50 p-4 rounded-xl text-blue-600 group-hover:bg-blue-100 transition-colors">
            <Users className="w-8 h-8" />
          </div>
          <div>
            <p className="text-slate-500 text-sm font-semibold uppercase tracking-wider mb-1">Total Student</p>
            <h3 className="text-3xl font-black text-slate-800">{report?.total_users || 0}</h3>
          </div>
        </Link>
        
        <Link to="/admin/users" className="bg-white p-6 rounded-2xl shadow-sm border border-slate-100 flex items-center space-x-4 hover:border-orange-400 transition-colors cursor-pointer group">
          <div className="bg-orange-50 p-4 rounded-xl text-orange-500 group-hover:bg-orange-100 transition-colors">
            <GraduationCap className="w-8 h-8" />
          </div>
          <div>
            <p className="text-slate-500 text-sm font-semibold uppercase tracking-wider mb-1">Total Instructor</p>
            <h3 className="text-3xl font-black text-slate-800">{report?.total_instructors || 0}</h3>
          </div>
        </Link>

        <Link to="/dashboard" className="bg-white p-6 rounded-2xl shadow-sm border border-slate-100 flex items-center space-x-4 hover:border-purple-400 transition-colors cursor-pointer group">
          <div className="bg-purple-50 p-4 rounded-xl text-purple-600 group-hover:bg-purple-100 transition-colors">
            <BookOpen className="w-8 h-8" />
          </div>
          <div>
            <p className="text-slate-500 text-sm font-semibold uppercase tracking-wider mb-1">Total Courses</p>
            <h3 className="text-3xl font-black text-slate-800">{report?.total_courses || 0}</h3>
          </div>
        </Link>

        <Link to="/admin/enrollments" className="bg-white p-6 rounded-2xl shadow-sm border border-slate-100 flex items-center space-x-4 hover:border-green-400 transition-colors cursor-pointer group">
          <div className="bg-green-50 p-4 rounded-xl text-green-600 group-hover:bg-green-100 transition-colors">
            <UserCheck className="w-8 h-8" />
          </div>
          <div>
            <p className="text-slate-500 text-sm font-semibold uppercase tracking-wider mb-1">Total Enrollments</p>
            <h3 className="text-3xl font-black text-slate-800">{report?.total_enrollments || 0}</h3>
          </div>
        </Link>
      </div>
    </div>
  );
}
