import { useState } from "react";
import BookingForm from "./components/BookingForm";
import BookingResult from "./components/BookingResult";
import LoadingSpinner from "./components/LoadingSpinner";

export default function App() {
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);

  async function handleBookingRequest(text) {
    setLoading(true);
    setResult(null);
    setError(null);

    try {
      const res = await fetch("/booking", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ request_text: text }),
      });

      if (!res.ok) {
        const body = await res.json().catch(() => null);
        throw new Error(body?.detail || `Request failed (${res.status})`);
      }

      setResult(await res.json());
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="container">
      <h1>Hotel AI Booking</h1>
      <p className="subtitle">
        Describe your stay in plain English and we'll find availability.
      </p>

      <BookingForm onSubmit={handleBookingRequest} disabled={loading} />

      {loading && <LoadingSpinner />}

      {error && <div className="error-banner">{error}</div>}

      {result && <BookingResult data={result} />}
    </div>
  );
}
