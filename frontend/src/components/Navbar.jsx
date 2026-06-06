export default function Navbar() {
  return (
    <nav className="bg-blue-900 text-white shadow-lg sticky top-0 z-50">
      <div className="max-w-7xl mx-auto px-6 h-20 flex justify-between items-center">

        {/* Logo */}

        <div>
          <h1 className="text-2xl font-bold tracking-wide">
            LoanPredict AI
          </h1>

          <p className="text-xs text-blue-200">
            AI Powered Loan Approval System
          </p>
        </div>

        {/* Navigation */}

        <div className="hidden md:flex items-center gap-8">

          <a
            href="#predict"
            className="hover:text-blue-200 transition font-medium"
          >
            Predict
          </a>

          <a
            href="#how"
            className="hover:text-blue-200 transition font-medium"
          >
            How It Works
          </a>

        </div>

      </div>
    </nav>
  );
}