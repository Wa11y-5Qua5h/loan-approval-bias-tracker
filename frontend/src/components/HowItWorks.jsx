export default function HowItWorks() {
  return (
    <section
      id="how"
      className="py-20 bg-white"
    >
      <div className="max-w-6xl mx-auto px-6">

        <h2 className="text-4xl font-bold text-center text-blue-900 mb-12">
          How It Works
        </h2>

        <div className="grid md:grid-cols-3 gap-8">

          <div className="bg-white border border-slate-200 shadow-md rounded-2xl p-8">
            <h3 className="text-xl font-bold text-blue-900">
              1. Enter Details
            </h3>

            <p className="mt-4 text-slate-600">
              Fill applicant and loan details.
            </p>
          </div>

          <div className="bg-white border border-slate-200 shadow-md rounded-2xl p-8">
            <h3 className="text-xl font-bold text-blue-900">
              2. AI Analysis
            </h3>

            <p className="mt-4 text-slate-600">
              ML model evaluates the application.
            </p>
          </div>

          <div className="bg-white border border-slate-200 shadow-md rounded-2xl p-8">
            <h3 className="text-xl font-bold text-blue-900">
              3. Get Prediction
            </h3>

            <p className="mt-4 text-slate-600">
              Receive approval probability instantly.
            </p>
          </div>

        </div>

      </div>
    </section>
  );
}