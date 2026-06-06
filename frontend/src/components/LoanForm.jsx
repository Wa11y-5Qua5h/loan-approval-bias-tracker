import axios from "axios";
import { useState } from "react";
import PredictionCard from "./PredictionCard";

export default function LoanForm() {
  const [prediction, setPrediction] = useState("");
  const [probability, setProbability] = useState(0);

  const [formData, setFormData] = useState({
    gender: "Male",
    married: "Yes",
    dependents: "0",
    education: "Graduate",
    selfEmployed: "No",
    applicantIncome: 50000,
    coApplicantIncome: 0,
    loanAmount: 150,
    loanTerm: 360,
    propertyArea: "Urban",
    creditHistory: "1",
  });

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });
  };

  const totalIncome =
    Number(formData.applicantIncome) +
    Number(formData.coApplicantIncome);

  const handlePredict = async (e) => {
  e.preventDefault();

  const payload = {
    Gender: formData.gender,
    Married: formData.married,
    Dependents: formData.dependents,
    Education: formData.education,
    Self_Employed: formData.selfEmployed,
    ApplicantIncome: Number(formData.applicantIncome),
    CoapplicantIncome: Number(formData.coApplicantIncome),
    LoanAmount: Number(formData.loanAmount),
    Loan_Amount_Term: Number(formData.loanTerm),
    Property_Area: formData.propertyArea,
    Credit_History: Number(formData.creditHistory),
  };

  try {
    const response = await axios.post(
      "http://localhost:5000/predict",
      payload
    );

    setPrediction(
      response.data.approved
        ? "Approved"
        : "Rejected"
    );

    setProbability(
      response.data.probability
    );

  } catch (error) {
    console.error(error);
    alert("Backend connection failed");
  }
};

  return (
    <section id="predict" className="py-12 px-4">
      <div className="max-w-7xl mx-auto">
        <div className="grid lg:grid-cols-3 gap-8">

          {/* FORM SECTION */}

          <div className="lg:col-span-2">

            <form
              onSubmit={handlePredict}
              className="space-y-8"
            >

              {/* PERSONAL INFORMATION */}

              <div className="bg-white border border-blue-100 shadow-md rounded-3xl p-6">

                <div className="mb-6">
                  <h2 className="text-blue-900 text-xl font-bold">
                    Personal Information
                  </h2>

                  <p className="text-slate-500 text-sm mt-1">
                    Provide applicant demographic details
                  </p>
                </div>

                <div className="grid md:grid-cols-3 gap-4">

                  <div>
                    <label className="block text-slate-600 mb-2">
                      Gender
                    </label>

                    <select
                      name="gender"
                      value={formData.gender}
                      onChange={handleChange}
                      className="bg-slate-50 border border-slate-300 text-slate-800 p-3 rounded-xl w-full"
                    >
                      <option value="Male">Male</option>
                      <option value="Female">Female</option>
                    </select>
                  </div>

                  <div>
                    <label className="block text-slate-600 mb-2">
                      Marital Status
                    </label>

                    <select
                      name="married"
                      value={formData.married}
                      onChange={handleChange}
className="bg-slate-50 border border-slate-300 text-slate-800 p-3 rounded-xl w-full"                    >
                      <option value="Yes">Yes</option>
                      <option value="No">No</option>
                    </select>
                  </div>

                  <div>
                    <label className="block text-slate-600 mb-2">
                      Dependents
                    </label>

                    <select
                      name="dependents"
                      value={formData.dependents}
                      onChange={handleChange}
className="bg-slate-50 border border-slate-300 text-slate-800 p-3 rounded-xl w-full"                    >
                      <option value="0">0</option>
                      <option value="1">1</option>
                      <option value="2">2</option>
                      <option value="3+">3+</option>
                    </select>
                  </div>

                  <div>
                    <label className="block text-slate-600 mb-2">
                      Education
                    </label>

                    <select
                      name="education"
                      value={formData.education}
                      onChange={handleChange}
className="bg-slate-50 border border-slate-300 text-slate-800 p-3 rounded-xl w-full"                    >
                      <option value="Graduate">Graduate</option>
                      <option value="Not Graduate">
                        Not Graduate
                      </option>
                    </select>
                  </div>

                  <div>
                    <label className="block text-slate-600 mb-2">
                      Self Employed
                    </label>

                    <select
                      name="selfEmployed"
                      value={formData.selfEmployed}
                      onChange={handleChange}
className="bg-slate-50 border border-slate-300 text-slate-800 p-3 rounded-xl w-full"                    >
                      <option value="No">No</option>
                      <option value="Yes">Yes</option>
                    </select>
                  </div>

                </div>

              </div>

              {/* INCOME DETAILS */}

              <div className="bg-white border border-blue-100 shadow-md rounded-3xl p-6">

                <div className="mb-6">
                  <h2 className="text-blue-900 text-xl font-bold">
                    Income Details
                  </h2>

                  <p className="text-slate-500 text-sm mt-1">
                    Monthly income details used for eligibility assessment
                  </p>
                </div>

                <div className="grid md:grid-cols-2 gap-4">

                  <div>
                    <label className="block text-slate-600 mb-2 text-sm">
                      Applicant Income (₹/month)
                    </label>

                    <input
                      type="number"
                      name="applicantIncome"
                      value={formData.applicantIncome}
                      onChange={handleChange}
                      className="bg-slate-50 border border-slate-300 text-slate-800 p-3 rounded-xl w-full"
                    />
                  </div>

                  <div>
                    <label className="block text-slate-600 mb-2 text-sm">
                      Co-Applicant Income (₹/month)
                    </label>

                    <input
                      type="number"
                      name="coApplicantIncome"
                      value={formData.coApplicantIncome}
                      onChange={handleChange}
                      className="bg-slate-50 border border-slate-300 text-slate-800 p-3 rounded-xl w-full"
                    />
                  </div>

                </div>

                <div className="mt-5 bg-blue-50 rounded-xl p-4">
                  <p className="text-blue-900 text-sm mb-1">
                    Total Household Income
                  </p>
<p className="text-blue-900 text-xl font-bold">
                  
                    ₹{totalIncome.toLocaleString()}/month
                  </p>
                </div>

              </div>

              {/* LOAN DETAILS */}

              <div className="bg-white border border-blue-100 shadow-md rounded-3xl p-6">

                <div className="mb-6">
                  <h2 className="text-blue-900 text-xl font-bold">
                    Loan Details
                  </h2>

                  <p className="text-slate-500 text-sm mt-1">
                    Specify the requested loan characteristics
                  </p>
                </div>

                <div className="grid md:grid-cols-3 gap-4">

                  <div>
                    <label className="block text-slate-600 mb-2 text-sm">
                      Loan Amount (₹ Thousands)
                    </label>

                    <input
                      type="number"
                      name="loanAmount"
                      value={formData.loanAmount}
                      onChange={handleChange}
                      className="bg-slate-50 border border-slate-300 text-slate-800 p-3 rounded-xl w-full"
                    />
                  </div>

                  <div>
                    <label className="block text-slate-600 mb-2 text-sm">
                      Loan Term (Months)
                    </label>

                    <input
                      type="number"
                      name="loanTerm"
                      value={formData.loanTerm}
                      onChange={handleChange}
                      className="bg-slate-50 border border-slate-300 text-slate-800 p-3 rounded-xl w-full"
                    />
                  </div>

                  <div>
                    <label className="block text-slate-600 mb-2 text-sm">
                      Property Area
                    </label>

                    <select
                      name="propertyArea"
                      value={formData.propertyArea}
                      onChange={handleChange}
className="bg-slate-50 border border-slate-300 text-slate-800 p-3 rounded-xl w-full"                    >
                      <option value="Urban">Urban</option>
                      <option value="Semiurban">
                        Semiurban
                      </option>
                      <option value="Rural">Rural</option>
                    </select>
                  </div>

                </div>

              </div>

              {/* CREDIT PROFILE */}

              <div className="bg-white border border-blue-100 shadow-md rounded-3xl p-6">

                <h2 className="text-blue-900 text-xl font-bold mb-6">
                  Credit Profile
                </h2>

                <label className="block text-slate-600 mb-2 text-sm">
                  Credit History
                </label>

                <select
                  name="creditHistory"
                  value={formData.creditHistory}
                  onChange={handleChange}
className="bg-slate-50 border border-slate-300 text-slate-800 p-3 rounded-xl w-full"                >
                  <option value="1">
                    Good Credit History
                  </option>

                  <option value="0">
                    Poor Credit History
                  </option>
                </select>

                <div className="mt-4 bg-blue-50 rounded-xl p-4">

                  <p className="text-slate-500 text-sm">
                    Credit History Impact
                  </p>

                  <p className="text-blue-800 font-semibold mt-1">
                    This is one of the most important factors affecting loan approval decisions.
                  </p>

                </div>

              </div>

              {/* BUTTON */}

              <button
                type="submit"
                className="w-full bg-blue-900 hover:bg-blue-800 text-white py-4 rounded-2xl text-lg font-bold transition"
              >
                Predict Loan Approval
              </button>

            </form>
          </div>

          {/* RESULT SECTION */}

          <div>
            <PredictionCard
              prediction={prediction}
              probability={probability}
            />
          </div>

        </div>
      </div>
    </section>
  );
}