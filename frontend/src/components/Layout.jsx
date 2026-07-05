import React from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { LogOut, BookOpen, LayoutDashboard, Compass, Heart, Users, BarChart3, Settings } from 'lucide-react';

const Layout = ({ children, user }) => {
  const navigate = useNavigate();

  const handleLogout = () => {
    localStorage.removeItem('token');
    navigate('/login');
  };

  const role = user?.role || 'student';

  // Define nav links based on role
  let navLinks = [];
  if (role === 'student') {
    navLinks = [
      { name: 'Dashboard', path: '/dashboard', icon: LayoutDashboard },
      { name: 'Catalog', path: '/courses', icon: Compass },
      { name: 'Wishlist', path: '/wishlist', icon: Heart },
    ];
  } else if (role === 'instructor') {
    navLinks = [
      { name: 'My Courses', path: '/instructor', icon: LayoutDashboard },
    ];
  } else if (role === 'admin') {
    navLinks = [
      { name: 'Analytics', path: '/admin', icon: BarChart3 },
      { name: 'Manage Courses', path: '/admin/courses', icon: Settings },
    ];
  }

  return (
    <div className="min-h-screen bg-apple-bg font-sans text-apple-dark">
      <nav className="bg-white/70 backdrop-blur-lg border-b border-white/20 sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between h-16">
            <div className="flex items-center space-x-6">
              <Link to={navLinks[0]?.path || '/'} className="flex items-center space-x-2">
                <div className="bg-apple-blue p-2 rounded-full shadow-sm">
                  <BookOpen className="h-5 w-5 text-white" />
                </div>
                <span className="text-xl font-bold tracking-tight">
                  Simple LMS
                </span>
              </Link>
              
              <div className="hidden md:flex space-x-1">
                {navLinks.map((link) => {
                  const Icon = link.icon;
                  return (
                    <Link
                      key={link.name}
                      to={link.path}
                      className="flex items-center space-x-1.5 px-3 py-2 rounded-full text-sm font-medium text-apple-gray hover:text-apple-dark hover:bg-black/5 transition-colors"
                    >
                      <Icon className="w-4 h-4" />
                      <span>{link.name}</span>
                    </Link>
                  )
                })}
              </div>
            </div>
            
            <div className="flex items-center space-x-4">
              <div className="flex items-center space-x-2 text-sm font-medium text-apple-dark bg-black/5 py-1.5 px-4 rounded-full">
                <Users className="w-4 h-4 text-apple-gray" />
                <span>{user?.username}</span>
                <span className="bg-white text-apple-dark text-xs font-semibold px-2.5 py-0.5 rounded-full uppercase tracking-wider shadow-sm">
                  {role}
                </span>
              </div>
              <button 
                onClick={handleLogout}
                className="flex items-center space-x-1 text-apple-gray hover:text-red-500 hover:bg-red-50 px-4 py-2 rounded-full transition-colors font-medium text-sm"
              >
                <LogOut className="w-4 h-4" />
                <span>Logout</span>
              </button>
            </div>
          </div>
        </div>
      </nav>

      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-10">
        {/* Pass user prop down if needed */}
        {React.cloneElement(children, { user })}
      </main>
    </div>
  );
};

export default Layout;
