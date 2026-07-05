import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { BookOpen, Sparkles, CheckCircle, Award, Compass } from 'lucide-react';
import { Link } from 'react-router-dom';

export default function Dashboard({ user }) {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchDashboard = async () => {
      try {
        const response = await axios.get('/api/v1/protected/dashboard/student');
        setData(response.data);
      } catch (error) {
        console.error('Error fetching dashboard data:', error);
      } finally {
        setLoading(false);
      }
    };
    fetchDashboard();
  }, []);

  if (loading) {
    return (
      <div className="flex justify-center py-20">
        <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-apple-dark"></div>
      </div>
    );
  }

  if (!data) {
    return (
      <div className="flex justify-center py-20">
        <p className="text-apple-gray font-medium">Data dashboard gagal dimuat. Silakan periksa koneksi atau login kembali.</p>
      </div>
    );
  }

  return (
    <div className="space-y-10 pb-12">
      {/* Header */}
      <div className="bg-white rounded-[32px] p-8 shadow-apple flex items-center justify-between border-0">
        <div>
          <h1 className="text-3xl font-bold tracking-tight text-apple-dark mb-1">
            Selamat datang, <span className="text-apple-blue">{user?.username}</span>!
          </h1>
          <p className="text-apple-gray font-medium">Lanjutkan progres belajar Anda hari ini.</p>
        </div>
        <div className="hidden md:flex bg-apple-bg p-4 rounded-3xl border border-black/5 items-center space-x-4">
          <Award className="w-10 h-10 text-apple-blue" />
          <div>
            <p className="text-sm font-bold text-apple-gray uppercase tracking-wider">Level</p>
            <p className="text-lg font-black text-apple-dark">Scholar</p>
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        {/* Kolom Kiri: Active & Completed Courses */}
        <div className="lg:col-span-2 space-y-10">
          
          {/* Active Courses */}
          <section>
            <div className="flex items-center space-x-2 mb-6">
              <BookOpen className="w-7 h-7 text-apple-blue" />
              <h2 className="text-2xl font-bold tracking-tight text-apple-dark">Sedang Dipelajari</h2>
            </div>
            
            {data?.active_courses.length === 0 ? (
              <div className="bg-white p-8 rounded-[32px] text-center shadow-apple border-0">
                <p className="text-apple-gray font-medium">Belum ada kursus yang sedang aktif.</p>
              </div>
            ) : (
              <div className="space-y-4">
                {data?.active_courses.map(course => (
                  <Link key={course.id} to={`/learn/${course.id}`} className="block bg-white p-6 rounded-[32px] shadow-apple border-0 hover:shadow-apple-lg transition-shadow">
                    <div className="flex justify-between items-start mb-5">
                      <div>
                        <h3 className="font-bold text-xl text-apple-dark mb-1">{course.title}</h3>
                        <p className="text-sm text-apple-gray font-medium">Instruktur: {course.instructor}</p>
                      </div>
                      <span className="font-black text-apple-blue text-xl bg-[#F0F0F2] px-3 py-1 rounded-2xl">
                        {course.progress_percentage}%
                      </span>
                    </div>
                    <div className="w-full bg-[#F0F0F2] rounded-full h-3 mb-1 overflow-hidden">
                      <div 
                        className="bg-apple-blue h-3 rounded-full transition-all duration-1000 ease-out" 
                        style={{ width: `${course.progress_percentage}%` }}
                      ></div>
                    </div>
                  </Link>
                ))}
              </div>
            )}
          </section>

          {/* Completed Courses */}
          <section>
            <div className="flex items-center space-x-2 mb-6">
              <CheckCircle className="w-7 h-7 text-green-500" />
              <h2 className="text-2xl font-bold tracking-tight text-apple-dark">Kursus Selesai</h2>
            </div>
            
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
              {data?.completed_courses.length === 0 ? (
                <div className="col-span-full bg-white p-6 rounded-[32px] text-center shadow-sm text-apple-gray font-medium">
                  Belum ada kursus yang diselesaikan.
                </div>
              ) : (
                data?.completed_courses.map(course => (
                  <Link key={course.id} to={`/course/${course.id}`} className="bg-white p-6 rounded-[32px] shadow-apple border-0 hover:shadow-apple-lg flex flex-col justify-center text-center transition-shadow">
                    <h3 className="font-bold text-apple-dark mb-2 leading-tight">{course.title}</h3>
                    <p className="text-xs font-semibold text-apple-gray">Oleh: {course.instructor}</p>
                  </Link>
                ))
              )}
            </div>
          </section>
        </div>

        {/* Kolom Kanan: Rekomendasi */}
        <div className="space-y-6">
          <div className="flex items-center space-x-2 mb-2">
            <Sparkles className="w-6 h-6 text-apple-gray" />
            <h2 className="text-2xl font-bold tracking-tight text-apple-dark">Rekomendasi Spesial</h2>
          </div>
          
          <div className="space-y-4">
            {data?.recommended_courses.length === 0 ? (
              <div className="bg-white p-6 rounded-[32px] text-center shadow-apple text-apple-gray font-medium">
                Tidak ada rekomendasi saat ini.
              </div>
            ) : (
              data?.recommended_courses.map(course => (
                <Link key={course.id} to={`/course/${course.id}`} className="block bg-white p-5 rounded-[28px] shadow-apple border-0 hover:shadow-apple-lg transition-all group">
                  <div className="flex flex-col">
                    <span className="inline-block px-3 py-1.5 bg-[#F0F0F2] text-apple-dark text-[10px] font-bold rounded-full uppercase tracking-wider mb-3 w-max">
                      {course.category || 'Umum'}
                    </span>
                    <h4 className="font-bold text-apple-dark text-base group-hover:text-apple-blue transition-colors line-clamp-2 mb-2">
                      {course.title}
                    </h4>
                    <p className="text-xs font-medium text-apple-gray">Instruktur: {course.instructor}</p>
                  </div>
                </Link>
              ))
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
