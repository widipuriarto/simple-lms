import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useParams, Link, useNavigate } from 'react-router-dom';
import { 
  BookOpen, Star, MessageSquare, ChevronLeft, 
  Layers, Clock, ShieldCheck, Heart, Trash2
} from 'lucide-react';

export default function CourseDetail({ user }) {
  const { id } = useParams();
  const navigate = useNavigate();
  const [course, setCourse] = useState(null);
  const [reviews, setReviews] = useState([]);
  const [comments, setComments] = useState([]);
  const [loading, setLoading] = useState(true);
  const [enrolling, setEnrolling] = useState(false);
  const [isEnrolled, setIsEnrolled] = useState(false);
  const [inWishlist, setInWishlist] = useState(false);
  
  // Forms
  const [newComment, setNewComment] = useState('');
  const [rating, setRating] = useState(5);
  const [reviewText, setReviewText] = useState('');

  useEffect(() => {
    fetchData();
  }, [id]);

  const fetchData = async () => {
    setLoading(true);
    try {
      // Fetch Course Detail
      const courseRes = await axios.get(`/api/v1/protected/courses/${id}`);
      setCourse(courseRes.data);

      // Fetch Reviews
      const reviewRes = await axios.get(`/api/v1/protected/courses/${id}/reviews`);
      setReviews(reviewRes.data.items || reviewRes.data);

      // Fetch Comments
      const commentRes = await axios.get(`/api/v1/protected/courses/${id}/comments`);
      setComments(commentRes.data.items || commentRes.data);

      // Check Enrollment Status & Wishlist if Student
      if (user?.role === 'student') {
        const myCoursesRes = await axios.get('/api/v1/protected/enrollments/my-courses');
        const enrolled = (myCoursesRes.data.items || myCoursesRes.data).some(c => c.course === courseRes.data.title);
        setIsEnrolled(enrolled);
        
        const wishlistRes = await axios.get('/api/v1/protected/wishlist');
        const isWished = (wishlistRes.data.items || wishlistRes.data).some(w => w.course.id === parseInt(id));
        setInWishlist(isWished);
      }
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleEnroll = async () => {
    setEnrolling(true);
    try {
      await axios.post(`/api/v1/protected/enrollments`, null, { params: { course_id: id } });
      setIsEnrolled(true);
      navigate(`/learn/${id}`);
    } catch (err) {
      alert("Gagal mendaftar kursus.");
    } finally {
      setEnrolling(false);
    }
  };

  const toggleWishlist = async () => {
    try {
      await axios.post(`/api/v1/protected/wishlist/${id}`);
      setInWishlist(!inWishlist);
    } catch (err) {
      console.error(err);
    }
  };

  const submitComment = async (e) => {
    e.preventDefault();
    if (!newComment.trim()) return;
    try {
      await axios.post(`/api/v1/protected/courses/${id}/comments`, { content: newComment });
      setNewComment('');
      fetchData(); // reload comments
    } catch (err) {
      alert("Gagal mengirim komentar.");
    }
  };

  const submitReview = async (e) => {
    e.preventDefault();
    if (!reviewText.trim()) return;
    try {
      await axios.post(`/api/v1/protected/courses/${id}/reviews`, { rating, comment: reviewText });
      setReviewText('');
      fetchData(); // reload reviews
    } catch (err) {
      alert(err.response?.data?.message || "Gagal mengirim review.");
    }
  };

  const deleteComment = async (commentId) => {
    if (!window.confirm("Hapus komentar ini?")) return;
    try {
      await axios.delete(`/api/v1/protected/comments/${commentId}`);
      fetchData(); // reload
    } catch (err) {
      alert("Gagal menghapus komentar.");
    }
  };

  if (loading) {
    return (
      <div className="flex justify-center py-20">
        <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-slate-800"></div>
      </div>
    );
  }

  if (!course) return <div>Kursus tidak ditemukan.</div>;

  return (
    <div className="space-y-8 pb-12">
      <Link to="/courses" className="inline-flex items-center text-sm text-slate-500 hover:text-slate-800 transition-colors">
        <ChevronLeft className="w-4 h-4 mr-1" /> Kembali ke Katalog
      </Link>

      {/* Hero Section */}
      <div className="bg-white rounded-3xl p-8 shadow-sm border border-slate-100">
        <div className="flex flex-col lg:flex-row justify-between gap-8">
          <div className="flex-1 space-y-4">
            <div className="flex items-center space-x-3">
              <span className="px-3 py-1 bg-slate-100 text-slate-700 text-xs font-bold rounded-full uppercase tracking-wider">
                {course.category || 'Umum'}
              </span>
              <span className="px-3 py-1 bg-green-50 text-green-700 text-xs font-bold rounded-full uppercase tracking-wider">
                {course.level || 'All Level'}
              </span>
            </div>
            
            <h1 className="text-4xl font-extrabold text-slate-900">{course.title}</h1>
            <p className="text-lg text-slate-600 leading-relaxed max-w-3xl">
              {course.description}
            </p>
            
            <div className="flex flex-wrap gap-4 pt-4 text-sm text-slate-500">
              <div className="flex items-center"><ShieldCheck className="w-4 h-4 mr-2" /> Instruktur: {course.instructor}</div>
              <div className="flex items-center"><Layers className="w-4 h-4 mr-2" /> {course.sections?.length || 0} Modul</div>
              <div className="flex items-center"><Star className="w-4 h-4 mr-2 text-yellow-500" /> {reviews.length} Ulasan</div>
            </div>
          </div>

          <div className="w-full lg:w-80 flex-shrink-0">
            <div className="bg-slate-50 rounded-2xl p-6 border border-slate-200 sticky top-24 text-center space-y-4">
              <div className="bg-white w-full aspect-video rounded-xl shadow-inner border border-slate-100 flex items-center justify-center mb-6">
                <BookOpen className="w-12 h-12 text-slate-300" />
              </div>
              
              {user?.role === 'student' && (
                <>
                  {isEnrolled ? (
                    <Link to={`/learn/${course.id}`} className="block w-full py-3 px-4 bg-slate-800 hover:bg-slate-900 text-white font-semibold rounded-xl transition-all shadow-md">
                      Lanjutkan Belajar
                    </Link>
                  ) : (
                    <button 
                      onClick={handleEnroll} 
                      disabled={enrolling}
                      className="w-full py-3 px-4 bg-slate-800 hover:bg-slate-900 text-white font-semibold rounded-xl transition-all shadow-md flex items-center justify-center"
                    >
                      {enrolling ? 'Mendaftar...' : 'Daftar Sekarang'}
                    </button>
                  )}
                  
                  <button 
                    onClick={toggleWishlist}
                    className={`w-full py-3 px-4 font-semibold rounded-xl transition-all border flex items-center justify-center space-x-2 ${inWishlist ? 'bg-red-50 text-red-600 border-red-200' : 'bg-white text-slate-700 border-slate-200 hover:bg-slate-50'}`}
                  >
                    <Heart className={`w-5 h-5 ${inWishlist ? 'fill-current' : ''}`} />
                    <span>{inWishlist ? 'Hapus dari Wishlist' : 'Tambah ke Wishlist'}</span>
                  </button>
                </>
              )}
            </div>
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        {/* Left Column: Curriculum */}
        <div className="lg:col-span-2 space-y-8">
          <div className="bg-white rounded-3xl p-8 shadow-sm border border-slate-100">
            <h2 className="text-2xl font-bold text-slate-900 mb-6">Silabus Kurikulum</h2>
            <div className="space-y-4">
              {course.sections?.map((section, idx) => (
                <div key={section.id} className="border border-slate-200 rounded-xl overflow-hidden">
                  <div className="bg-slate-50 px-6 py-4 font-semibold text-slate-800 border-b border-slate-200">
                    Modul {idx + 1}: {section.title}
                  </div>
                  <div className="divide-y divide-slate-100 bg-white">
                    {section.lessons?.map((lesson, l_idx) => (
                      <div key={lesson.id} className="px-6 py-4 text-slate-600 flex items-center">
                        <Clock className="w-4 h-4 mr-3 text-slate-400" />
                        <span>Materi {l_idx + 1}: {lesson.title}</span>
                      </div>
                    ))}
                  </div>
                </div>
              ))}
            </div>
          </div>
          
          {/* Discussion / Comments */}
          <div className="bg-white rounded-3xl p-8 shadow-sm border border-slate-100">
            <div className="flex items-center space-x-2 mb-6">
              <MessageSquare className="w-6 h-6 text-slate-700" />
              <h2 className="text-2xl font-bold text-slate-900">Ruang Diskusi</h2>
            </div>
            
            <form onSubmit={submitComment} className="mb-8">
              <textarea
                value={newComment}
                onChange={(e) => setNewComment(e.target.value)}
                placeholder="Tuliskan pertanyaan atau komentar Anda..."
                className="w-full p-4 border border-slate-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-slate-400 focus:border-transparent bg-slate-50 resize-none"
                rows="3"
                required
              ></textarea>
              <div className="mt-2 flex justify-end">
                <button type="submit" className="px-6 py-2 bg-slate-800 text-white rounded-lg text-sm font-medium hover:bg-slate-900">
                  Kirim Komentar
                </button>
              </div>
            </form>

            <div className="space-y-4">
              {comments.length === 0 ? (
                <p className="text-center text-slate-500 italic py-4">Belum ada diskusi.</p>
              ) : (
                comments.map(c => (
                  <div key={c.id} className="bg-slate-50 p-4 rounded-xl border border-slate-100">
                    <div className="flex justify-between items-center mb-2">
                      <span className="font-semibold text-slate-800">{c.user}</span>
                      <div className="flex items-center space-x-3">
                        <span className="text-xs text-slate-400">{c.created_at}</span>
                        {(user?.role === 'admin' || user?.username === c.user) && (
                          <button 
                            onClick={() => deleteComment(c.id)}
                            className="text-red-500 hover:text-red-700 transition-colors"
                            title="Hapus Komentar"
                          >
                            <Trash2 className="w-4 h-4" />
                          </button>
                        )}
                      </div>
                    </div>
                    <p className="text-slate-600 text-sm leading-relaxed">{c.content}</p>
                  </div>
                ))
              )}
            </div>
          </div>
        </div>

        {/* Right Column: Reviews */}
        <div className="space-y-8">
          <div className="bg-white rounded-3xl p-8 shadow-sm border border-slate-100">
            <div className="flex items-center space-x-2 mb-6">
              <Star className="w-6 h-6 text-yellow-500" />
              <h2 className="text-2xl font-bold text-slate-900">Ulasan</h2>
            </div>

            {isEnrolled && (
              <form onSubmit={submitReview} className="mb-8 border-b border-slate-100 pb-6">
                <h3 className="font-semibold text-sm mb-2 text-slate-700">Tulis Ulasan Anda</h3>
                <div className="flex mb-3">
                  {[1,2,3,4,5].map(num => (
                    <Star 
                      key={num} 
                      className={`w-6 h-6 cursor-pointer ${num <= rating ? 'text-yellow-500 fill-current' : 'text-slate-300'}`}
                      onClick={() => setRating(num)}
                    />
                  ))}
                </div>
                <textarea
                  value={reviewText}
                  onChange={(e) => setReviewText(e.target.value)}
                  placeholder="Ceritakan pengalaman belajar Anda..."
                  className="w-full p-3 border border-slate-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-slate-400 text-sm bg-slate-50 resize-none mb-2"
                  rows="2"
                  required
                ></textarea>
                <button type="submit" className="w-full px-4 py-2 bg-slate-200 text-slate-800 rounded-lg text-sm font-semibold hover:bg-slate-300">
                  Kirim Ulasan
                </button>
              </form>
            )}

            <div className="space-y-4">
              {reviews.length === 0 ? (
                <p className="text-center text-slate-500 italic text-sm py-2">Belum ada ulasan.</p>
              ) : (
                reviews.map((r, idx) => (
                  <div key={idx} className="bg-white p-4 rounded-xl border border-slate-100 shadow-sm">
                    <div className="flex items-center mb-2">
                      <span className="font-bold text-slate-800 mr-2">{r.user || 'Siswa'}</span>
                      <div className="flex">
                        {[...Array(r.rating)].map((_, i) => (
                          <Star key={i} className="w-3 h-3 text-yellow-500 fill-current" />
                        ))}
                      </div>
                    </div>
                    <p className="text-slate-600 text-sm italic">"{r.comment}"</p>
                  </div>
                ))
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
