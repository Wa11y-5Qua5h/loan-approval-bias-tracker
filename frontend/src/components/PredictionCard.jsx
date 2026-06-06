export default function PredictionCard({
  prediction,
  probability,
}) {
  if (!prediction) {
    return (
      <div className="bg-white border border-slate-200 shadow-md rounded-3xl p-8 sticky top-6">

        <h2 className="text-2xl font-bold mb-4 text-blue-900">
          Prediction Result
        </h2>

        <p className="text-slate-500">
          Complete the application form and click
          predict to see the AI analysis.
        </p>

      </div>
    );
  }

  return (
    <div className="space-y-6 sticky top-6">

      <div className="bg-white border border-slate-200 shadow-md rounded-3xl p-8">

        <h2 className="text-xl text-slate-500 mb-3">
          Prediction Result
        </h2>

        <h1
          className={`text-5xl font-bold ${
            prediction === "Approved"
              ? "text-green-600"
              : "text-red-600"
          }`}
        >
          {prediction}
        </h1>

        <p className="mt-4 text-slate-500">
          Approval Probability
        </p>

        <div className="w-full bg-slate-200 h-3 rounded-full mt-4">
          <div
            className="bg-blue-900 h-3 rounded-full"
            style={{
              width: `${probability}%`,
            }}
          />
        </div>

        <p className="text-right mt-2 text-slate-800 font-semibold">
          {probability}%
        </p>

      </div>

      <div className="bg-white border border-slate-200 shadow-md rounded-3xl p-6">

        <h3 className="font-bold text-blue-900 mb-4">
          Confidence Level
        </h3>

        <span className="bg-blue-100 text-blue-900 px-4 py-2 rounded-xl">
          High Confidence
        </span>

      </div>

      <div className="bg-white border border-slate-200 shadow-md rounded-3xl p-6">

        <h3 className="font-bold text-blue-900 mb-4">
          Key Factors
        </h3>

        <ul className="space-y-3 text-slate-600">
          <li>✔ Strong Credit History</li>
          <li>✔ Stable Income</li>
          <li>✔ Suitable Loan Amount</li>
        </ul>

      </div>

    </div>
  );
}