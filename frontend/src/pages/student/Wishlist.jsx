import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Link } from 'react-router-dom';
import { Heart, BookOpen, Trash2 } from 'lucide-react';

export default function Wishlist() {
  const [wishlist, setWishlist] = useState([]);
  const [loading, setLoading] = useState(true);

  const fetchWishlist = async () => {
    setLoading(true);
    try {
      const res = await axios.get('/api/v1/protected/wishlist');
      setWishlist(res.data.items || res.data);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchWishlist();
  }, []);

  const removeWishlist = async (courseId) => {
    try {
      await axios.post(`/api/v1/protected/wishlist/${courseId}`);
      fetchWishlist();
    } catch (err) {
      alert("Gagal menghapus.");
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
      <div className="flex items-center space-x-3">
        <Heart className="w-8 h-8 text-red-500 fill-current" />
        <h1 className="text-3xl font-bold tracking-tight text-apple-dark">Wishlist Saya</h1>
      </div>

      {wishlist.length === 0 ? (
        <div className="text-center py-20 bg-white rounded-3xl border border-slate-100 shadow-sm">
          <BookOpen className="w-16 h-16 text-slate-200 mx-auto mb-4" />
          <h3 className="text-xl font-bold text-slate-800">Wishlist Kosong</h3>
          <p className="text-slate-500 mt-2">Anda belum menyimpan kursus apapun ke dalam daftar favorit.</p>
          <Link to="/courses" className="mt-6 inline-block bg-slate-800 text-white px-6 py-2 rounded-lg font-medium hover:bg-slate-900 transition-colors">
            Jelajahi Kursus
          </Link>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {wishlist.map((item) => (
            <div key={item.id} className="bg-white rounded-[32px] p-6 shadow-apple border-0 relative group flex flex-col hover:shadow-apple-lg transition-all">
              <button 
                onClick={() => removeWishlist(item.course_id)}
                className="absolute top-6 right-6 p-2 bg-red-50 text-red-500 rounded-full hover:bg-red-100 transition-colors opacity-0 group-hover:opacity-100"
                title="Hapus dari Wishlist"
              >
                <Trash2 className="w-5 h-5" />
              </button>
              
              <div className="flex-grow pt-2">
                <span className="inline-block px-3 py-1 bg-[#F0F0F2] text-apple-dark text-xs font-bold rounded-full uppercase tracking-wider mb-4">
                  Kursus Disimpan
                </span>
                <Link to={`/course/${item.course_id}`}>
                  <h3 className="font-bold text-xl text-apple-dark mb-2 hover:text-apple-blue transition-colors line-clamp-2">
                    {item.course_title}
                  </h3>
                </Link>
                <p className="text-sm text-apple-gray font-medium mb-4">Disimpan: {new Date(item.created_at).toLocaleDateString()}</p>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
