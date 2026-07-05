import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Trash2, ShieldAlert } from 'lucide-react';
import { Link } from 'react-router-dom';

export default function AdminCourses() {
  const [courses, setCourses] = useState([]);
  const [loading, setLoading] = useState(true);

  const fetchCourses = async () => {
    try {
      const res = await axios.get('/api/v1/protected/courses');
      setCourses(res.data.items || res.data);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchCourses();
  }, []);

  const handleDelete = async (courseId) => {
    if (!window.confirm("PERINGATAN: Hapus kursus secara permanen?")) return;
    
    try {
      await axios.delete(`/api/v1/protected/courses/${courseId}`);
      fetchCourses(); // refresh
    } catch (err) {
      alert("Gagal menghapus kursus.");
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
      <div className="bg-white p-8 rounded-3xl shadow-sm border border-slate-100 flex items-center space-x-4">
        <ShieldAlert className="w-12 h-12 text-red-500" />
        <div>
          <h1 className="text-3xl font-extrabold text-slate-900 mb-2">Moderation Center</h1>
          <p className="text-slate-500">Anda memiliki hak akses penuh untuk menghapus kursus secara sepihak.</p>
        </div>
      </div>

      <div className="bg-white rounded-3xl overflow-hidden shadow-sm border border-slate-100">
        <div className="overflow-x-auto">
          <table className="w-full text-left border-collapse">
            <thead>
              <tr className="bg-slate-50 border-b border-slate-200 text-slate-500 text-sm uppercase tracking-wider">
                <th className="p-4 font-semibold">ID</th>
                <th className="p-4 font-semibold">Judul Kursus</th>
                <th className="p-4 font-semibold">Instruktur</th>
                <th className="p-4 font-semibold">Kategori</th>
                <th className="p-4 font-semibold text-right">Aksi Moderasi</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100 text-sm">
              {courses.map(course => (
                <tr key={course.id} className="hover:bg-slate-50 transition-colors">
                  <td className="p-4 font-medium text-slate-900">#{course.id}</td>
                  <td className="p-4">
                    <Link to={`/course/${course.id}`} className="font-bold text-slate-800 hover:text-slate-600 line-clamp-1">
                      {course.title}
                    </Link>
                  </td>
                  <td className="p-4 text-slate-600">{course.instructor}</td>
                  <td className="p-4 text-slate-600">{course.category || 'Umum'}</td>
                  <td className="p-4 text-right">
                    <button 
                      onClick={() => handleDelete(course.id)}
                      className="inline-flex items-center px-3 py-1.5 bg-red-50 text-red-600 hover:bg-red-100 rounded-lg font-semibold transition-colors"
                    >
                      <Trash2 className="w-4 h-4 mr-1" /> Hapus Paksa
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
          {courses.length === 0 && (
            <div className="p-8 text-center text-slate-500">Tidak ada kursus di dalam sistem.</div>
          )}
        </div>
      </div>
    </div>
  );
}
