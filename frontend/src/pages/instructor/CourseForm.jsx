import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useParams, useNavigate, Link } from 'react-router-dom';
import { ChevronLeft, Save } from 'lucide-react';

export default function CourseForm() {
  const { id } = useParams();
  const navigate = useNavigate();
  const isEdit = !!id;

  const [title, setTitle] = useState('');
  const [description, setDescription] = useState('');
  const [loading, setLoading] = useState(isEdit);
  const [saving, setSaving] = useState(false);

  useEffect(() => {
    if (isEdit) {
      const fetchCourse = async () => {
        try {
          const res = await axios.get(`/api/v1/protected/courses/${id}`);
          setTitle(res.data.title);
          setDescription(res.data.description);
        } catch (err) {
          alert("Gagal memuat kursus");
        } finally {
          setLoading(false);
        }
      };
      fetchCourse();
    }
  }, [id, isEdit]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setSaving(true);
    try {
      if (isEdit) {
        await axios.patch(`/api/v1/protected/courses/${id}`, { title, description });
      } else {
        await axios.post('/api/v1/protected/courses', { title, description });
      }
      navigate('/instructor');
    } catch (err) {
      alert("Gagal menyimpan kursus");
    } finally {
      setSaving(false);
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
    <div className="max-w-2xl mx-auto space-y-6">
      <Link to="/instructor" className="inline-flex items-center text-sm text-slate-500 hover:text-slate-800 transition-colors">
        <ChevronLeft className="w-4 h-4 mr-1" /> Kembali ke Dashboard
      </Link>

      <div className="bg-white rounded-3xl p-8 shadow-sm border border-slate-100">
        <h1 className="text-2xl font-extrabold text-slate-900 mb-6">
          {isEdit ? 'Edit Kursus' : 'Buat Kursus Baru'}
        </h1>

        <form onSubmit={handleSubmit} className="space-y-6">
          <div className="space-y-2">
            <label className="text-sm font-semibold text-slate-700">Judul Kursus</label>
            <input
              type="text"
              value={title}
              onChange={(e) => setTitle(e.target.value)}
              className="w-full px-4 py-3 border border-slate-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-slate-400 focus:border-transparent bg-slate-50"
              placeholder="Contoh: Belajar React Modern"
              required
            />
          </div>

          <div className="space-y-2">
            <label className="text-sm font-semibold text-slate-700">Deskripsi Lengkap</label>
            <textarea
              value={description}
              onChange={(e) => setDescription(e.target.value)}
              className="w-full px-4 py-3 border border-slate-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-slate-400 focus:border-transparent bg-slate-50 resize-none"
              placeholder="Jelaskan apa saja yang akan dipelajari..."
              rows="6"
              required
            ></textarea>
          </div>

          <div className="pt-4 border-t border-slate-100">
            <button
              type="submit"
              disabled={saving}
              className="flex items-center justify-center w-full py-3 px-4 bg-slate-800 hover:bg-slate-900 text-white font-semibold rounded-xl transition-all shadow-md"
            >
              <Save className="w-5 h-5 mr-2" />
              {saving ? 'Menyimpan...' : 'Simpan Kursus'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}
