import React from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';

// Core
import Login from './pages/Login';
import ProtectedRoute from './components/ProtectedRoute';
import Layout from './components/Layout';

// Student
import Dashboard from './pages/Dashboard';
import CourseCatalog from './pages/student/CourseCatalog';
import CourseDetail from './pages/student/CourseDetail';
import LearningRoom from './pages/student/LearningRoom';
import Wishlist from './pages/student/Wishlist';

// Instructor
import InstructorDashboard from './pages/instructor/InstructorDashboard';
import CourseForm from './pages/instructor/CourseForm';

// Admin
import AdminDashboard from './pages/admin/AdminDashboard';
import AdminCourses from './pages/admin/AdminCourses';
import AdminUsers from './pages/admin/AdminUsers';
import AdminEnrollments from './pages/admin/AdminEnrollments';

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Navigate to="/login" replace />} />
        <Route path="/login" element={<Login />} />
        
        {/* === STUDENT ROUTES === */}
        <Route path="/dashboard" element={<ProtectedRoute allowedRoles={['student']}><Layout><Dashboard /></Layout></ProtectedRoute>} />
        <Route path="/courses" element={<ProtectedRoute allowedRoles={['student']}><Layout><CourseCatalog /></Layout></ProtectedRoute>} />
        <Route path="/course/:id" element={<ProtectedRoute allowedRoles={['student', 'instructor', 'admin']}><Layout><CourseDetail /></Layout></ProtectedRoute>} />
        <Route path="/learn/:id" element={<ProtectedRoute allowedRoles={['student']}><Layout><LearningRoom /></Layout></ProtectedRoute>} />
        <Route path="/wishlist" element={<ProtectedRoute allowedRoles={['student']}><Layout><Wishlist /></Layout></ProtectedRoute>} />

        {/* === INSTRUCTOR ROUTES === */}
        <Route path="/instructor" element={<ProtectedRoute allowedRoles={['instructor']}><Layout><InstructorDashboard /></Layout></ProtectedRoute>} />
        <Route path="/instructor/course/create" element={<ProtectedRoute allowedRoles={['instructor']}><Layout><CourseForm /></Layout></ProtectedRoute>} />
        <Route path="/instructor/course/edit/:id" element={<ProtectedRoute allowedRoles={['instructor']}><Layout><CourseForm /></Layout></ProtectedRoute>} />

        {/* === ADMIN ROUTES === */}
        <Route path="/admin" element={<ProtectedRoute allowedRoles={['admin']}><Layout><AdminDashboard /></Layout></ProtectedRoute>} />
        <Route path="/admin/courses" element={<ProtectedRoute allowedRoles={['admin']}><Layout><AdminCourses /></Layout></ProtectedRoute>} />
        <Route path="/admin/users" element={<ProtectedRoute allowedRoles={['admin']}><Layout><AdminUsers /></Layout></ProtectedRoute>} />
        <Route path="/admin/enrollments" element={<ProtectedRoute allowedRoles={['admin']}><Layout><AdminEnrollments /></Layout></ProtectedRoute>} />

    </Routes>
    </BrowserRouter>
  );
}

export default App;
