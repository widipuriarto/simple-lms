import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Link } from 'react-router-dom';
import { Search, Filter, BookOpen } from 'lucide-react';

export default function CourseCatalog() {
  const [courses, setCourses] = useState([]);
  const [loading, setLoading] = useState(true);
  const [search, setSearch] = useState('');
  const [level, setLevel] = useState('');
  const [status, setStatus] = useState('published'); // default only published

  useEffect(() => {
    const fetchCourses = async () => {
      setLoading(true);
      try {
        const params = {};
        if (search) params.search = search;
        if (level) params.level = level;
        if (status) params.status = status;
        
        const res = await axios.get('/api/v1/protected/courses', { params });
        setCourses(res.data.items || res.data); // Handle pagination structure if any
      } catch (err) {
        console.error('Error fetching courses:', err);
      } finally {
        setLoading(false);
      }
    };
    
    // Add simple debounce
    const timeoutId = setTimeout(() => {
      fetchCourses();
    }, 500);
    return () => clearTimeout(timeoutId);
  }, [search, level, status]);

  return (
    <div className="space-y-6">
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
        <h1 className="text-3xl font-bold tracking-tight text-apple-dark">Katalog Kursus</h1>
        
        <div className="flex flex-col sm:flex-row gap-3 w-full md:w-auto">
          <div className="relative flex-grow sm:max-w-xs">
            <div className="absolute inset-y-0 left-0 pl-4 flex items-center pointer-events-none">
              <Search className="h-5 w-5 text-apple-gray/70" />
            </div>
            <input
              type="text"
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              placeholder="Cari kursus..."
              className="w-full pl-11 pr-4 py-3 border-0 rounded-full focus:outline-none focus:ring-2 focus:ring-apple-blue bg-[#F0F0F2] text-apple-dark font-medium transition-all"
            />
          </div>
          
          <select 
            value={level} 
            onChange={(e) => setLevel(e.target.value)}
            className="px-5 py-3 border-0 rounded-full font-medium text-apple-dark bg-[#F0F0F2] focus:outline-none focus:ring-2 focus:ring-apple-blue transition-all"
          >
            <option value="">Semua Level</option>
            <option value="beginner">Beginner</option>
            <option value="intermediate">Intermediate</option>
            <option value="advanced">Advanced</option>
          </select>
        </div>
      </div>

      {loading ? (
        <div className="flex justify-center py-20">
          <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-apple-dark"></div>
        </div>
      ) : courses.length === 0 ? (
        <div className="text-center py-24 bg-white rounded-[32px] border-0 shadow-apple">
          <BookOpen className="w-14 h-14 text-apple-gray/30 mx-auto mb-4" />
          <h3 className="text-xl font-bold text-apple-dark">Tidak ada kursus ditemukan</h3>
          <p className="text-apple-gray font-medium mt-1">Coba ubah kata kunci pencarian atau filter Anda.</p>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {courses.map((course) => (
            <Link 
              key={course.id} 
              to={`/course/${course.id}`}
              className="bg-white rounded-[32px] p-6 shadow-apple hover:shadow-apple-lg transition-all border-0 group flex flex-col h-full"
            >
              <div className="flex-grow">
                <div className="flex justify-between items-start mb-4">
                  <span className="inline-block px-3 py-1.5 bg-[#F0F0F2] text-apple-dark text-xs font-bold rounded-full uppercase tracking-wider">
                    {course.category || 'Umum'}
                  </span>
                </div>
                <h3 className="font-bold text-xl text-apple-dark mb-2 group-hover:text-apple-blue transition-colors line-clamp-2">
                  {course.title}
                </h3>
                <p className="text-sm text-apple-gray font-medium line-clamp-3 mb-4">
                  {course.description || 'Tidak ada deskripsi.'}
                </p>
              </div>
              
              <div className="pt-4 border-t border-black/5 mt-auto flex justify-between items-center text-sm text-apple-gray">
                <span className="font-bold">{course.instructor}</span>
              </div>
            </Link>
          ))}
        </div>
      )}
    </div>
  );
}
