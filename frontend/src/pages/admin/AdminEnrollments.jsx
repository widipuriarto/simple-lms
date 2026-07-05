import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Link } from 'react-router-dom';
import { UserCheck, ChevronLeft, Search, Calendar, Book } from 'lucide-react';

export default function AdminEnrollments() {
  const [enrollments, setEnrollments] = useState([]);
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState('');

  useEffect(() => {
    const fetchEnrollments = async () => {
      try {
        const res = await axios.get('/api/v1/protected/admin/enrollments');
        setEnrollments(res.data);
      } catch (err) {
        console.error(err);
      } finally {
        setLoading(false);
      }
    };
    fetchEnrollments();
  }, []);

  const filteredEnrollments = enrollments.filter(e => 
    e.user.toLowerCase().includes(searchTerm.toLowerCase()) || 
    e.course_title.toLowerCase().includes(searchTerm.toLowerCase())
  );

  if (loading) {
    return (
      <div className="flex justify-center items-center py-40">
        <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-apple-blue"></div>
      </div>
    );
  }

  return (
    <div className="space-y-6 animate-fade-in max-w-6xl mx-auto pb-12">
      <Link to="/admin" className="inline-flex items-center text-sm font-semibold text-apple-gray hover:text-apple-dark transition-colors mb-2">
        <ChevronLeft className="w-4 h-4 mr-1" /> Kembali ke Analytics
      </Link>
      
      <div className="bg-white/70 backdrop-blur-xl p-8 rounded-[32px] shadow-apple border border-white flex flex-col md:flex-row justify-between items-start md:items-center gap-6">
        <div className="flex items-center space-x-4">
          <div className="bg-green-50 p-4 rounded-2xl text-green-600">
            <UserCheck className="w-8 h-8" />
          </div>
          <div>
            <h1 className="text-3xl font-bold text-apple-dark mb-1">Daftar Pendaftaran</h1>
            <p className="text-apple-gray font-medium">Lihat seluruh riwayat pendaftaran kursus (Enrollments).</p>
          </div>
        </div>
        
        <div className="relative w-full md:w-72">
          <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
            <Search className="h-5 w-5 text-gray-400" />
          </div>
          <input
            type="text"
            className="w-full pl-10 pr-4 py-3 rounded-2xl border-0 focus:ring-2 focus:ring-apple-blue bg-[#F0F0F2] text-apple-dark transition-all"
            placeholder="Cari pengguna/kursus..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
          />
        </div>
      </div>

      <div className="bg-white/80 backdrop-blur-xl rounded-[32px] shadow-apple border border-white overflow-hidden">
        <div className="overflow-x-auto">
          <table className="w-full text-left border-collapse">
            <thead>
              <tr className="bg-gray-50/50 border-b border-gray-100">
                <th className="px-6 py-5 text-sm font-semibold text-gray-500 uppercase tracking-wider">ID</th>
                <th className="px-6 py-5 text-sm font-semibold text-gray-500 uppercase tracking-wider">Student</th>
                <th className="px-6 py-5 text-sm font-semibold text-gray-500 uppercase tracking-wider">Kursus</th>
                <th className="px-6 py-5 text-sm font-semibold text-gray-500 uppercase tracking-wider">Tanggal Daftar</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-100">
              {filteredEnrollments.map(enrollment => (
                <tr key={enrollment.id} className="hover:bg-gray-50/50 transition-colors">
                  <td className="px-6 py-5 text-sm font-medium text-gray-900">#{enrollment.id}</td>
                  <td className="px-6 py-5 text-sm font-semibold text-apple-dark">
                    {enrollment.user}
                  </td>
                  <td className="px-6 py-5 text-sm font-medium text-apple-blue flex items-center gap-2">
                    <Book className="w-4 h-4 text-apple-blue/60" />
                    {enrollment.course_title}
                  </td>
                  <td className="px-6 py-5 text-sm text-gray-500 flex items-center gap-2">
                    <Calendar className="w-4 h-4" />
                    {new Date(enrollment.enrolled_at).toLocaleDateString('id-ID', {
                      year: 'numeric', month: 'long', day: 'numeric',
                      hour: '2-digit', minute: '2-digit'
                    })}
                  </td>
                </tr>
              ))}
              {filteredEnrollments.length === 0 && (
                <tr>
                  <td colSpan="4" className="px-6 py-10 text-center text-gray-500">
                    Tidak ada data pendaftaran yang ditemukan.
                  </td>
                </tr>
              )}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
