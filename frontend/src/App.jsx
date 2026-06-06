import Navbar from "./components/Navbar";
import Hero from "./components/Hero";
import LoanForm from "./components/LoanForm";
import HowItWorks from "./components/HowItWorks";
import Footer from "./components/Footer";

function App() {
  return (
    <div className="bg-white min-h-screen">
      <Navbar />
      <Hero />
      <LoanForm />
      <HowItWorks />
      <Footer />
    </div>
  );
}

export default App;