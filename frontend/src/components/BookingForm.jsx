import { useState } from "react";

export default function BookingForm({ onSubmit, disabled }) {
  const [text, setText] = useState("");

  function handleSubmit(e) {
    e.preventDefault();
    if (text.trim()) onSubmit(text.trim());
  }

  return (
    <form className="booking-form" onSubmit={handleSubmit}>
      <textarea
        value={text}
        onChange={(e) => setText(e.target.value)}
        placeholder='e.g. "Book a room for John Smith, 2 guests, checking in June 10 and checking out June 14"'
        disabled={disabled}
      />
      <button type="submit" disabled={disabled || !text.trim()}>
        Check Availability
      </button>
    </form>
  );
}
