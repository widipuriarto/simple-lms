import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Link } from 'react-router-dom';
import { Plus, Edit, BookOpen } from 'lucide-react';

export default function InstructorDashboard({ user }) {
  const [courses, setCourses] = useState([]);
  const [loading, setLoading] = useState(true);

  const fetchCourses = async () => {
    try {
      // API list_courses support filter by instructor
      const res = await axios.get('/api/v1/protected/courses', {
        params: { instructor: user?.username }
      });
      setCourses(res.data.items || res.data);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    if (user?.username) fetchCourses();
  }, [user]);

  if (loading) {
    return (
      <div className="flex justify-center py-20">
        <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-slate-800"></div>
      </div>
    );
  }

  return (
    <div className="space-y-8">
      <div className="flex justify-between items-center bg-white p-8 rounded-3xl shadow-sm border border-slate-100">
        <div>
          <h1 className="text-3xl font-extrabold text-slate-900 mb-2">Instructor Dashboard</h1>
          <p className="text-slate-500">Kelola dan pantau seluruh kursus yang Anda publikasikan.</p>
        </div>
        <Link 
          to="/instructor/course/create"
          className="flex items-center space-x-2 bg-slate-800 hover:bg-slate-900 text-white px-6 py-3 rounded-xl font-semibold transition-colors shadow-md"
        >
          <Plus className="w-5 h-5" />
          <span>Buat Kursus Baru</span>
        </Link>
      </div>

      {courses.length === 0 ? (
        <div className="text-center py-20 bg-white rounded-3xl border border-slate-100 shadow-sm">
          <BookOpen className="w-16 h-16 text-slate-200 mx-auto mb-4" />
          <h3 className="text-xl font-bold text-slate-800">Belum ada kursus</h3>
          <p className="text-slate-500 mt-2">Mulai bagikan ilmu Anda dengan membuat kursus pertama.</p>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {courses.map(course => (
            <div key={course.id} className="bg-white rounded-2xl p-6 shadow-sm border border-slate-100 flex flex-col">
              <div className="flex-grow mb-4">
                <span className="inline-block px-3 py-1 bg-slate-100 text-slate-700 text-xs font-bold rounded-full uppercase tracking-wider mb-3">
                  {course.category || 'Umum'}
                </span>
                <h3 className="font-bold text-xl text-slate-900 mb-2 line-clamp-2">{course.title}</h3>
                <p className="text-sm text-slate-500 line-clamp-3">{course.description || 'Tidak ada deskripsi.'}</p>
              </div>
              <div className="pt-4 border-t border-slate-100 flex justify-end">
                <Link 
                  to={`/instructor/course/edit/${course.id}`}
                  className="flex items-center space-x-1 text-sm font-semibold text-slate-600 hover:text-slate-900 bg-slate-100 hover:bg-slate-200 px-4 py-2 rounded-lg transition-colors"
                >
                  <Edit className="w-4 h-4" />
                  <span>Edit Kursus</span>
                </Link>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
