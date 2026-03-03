import SplitStayCard from "./SplitStayCard";

export default function BookingResult({ data }) {
  const available = data.booking_possible;

  return (
    <div className={`result-card ${available ? "" : "unavailable"}`}>
      <h2>{available ? "Rooms Available" : "No Availability"}</h2>

      <div className="detail-row">
        <span className="label">Guest</span>
        <span>{data.guest_name}</span>
      </div>
      <div className="detail-row">
        <span className="label">Check-in</span>
        <span>{data.check_in}</span>
      </div>
      <div className="detail-row">
        <span className="label">Check-out</span>
        <span>{data.check_out}</span>
      </div>
      <div className="detail-row">
        <span className="label">Guests</span>
        <span>{data.num_guests}</span>
      </div>
      <div className="detail-row">
        <span className="label">Nights</span>
        <span>{data.stay_nights}</span>
      </div>

      {data.available_rooms.length > 0 && (
        <ul className="rooms-list">
          {data.available_rooms.map((room) => (
            <li key={room}>{room}</li>
          ))}
        </ul>
      )}

      {data.split_stay && <SplitStayCard segments={data.split_stay} />}

      {data.discount_applied && (
        <div className="discount-badge">
          {data.discount_applied.percentage}% off (stay {">="}{" "}
          {data.discount_applied.nights_threshold} nights)
        </div>
      )}

      {available && <div className="price">${data.estimated_price}</div>}
    </div>
  );
}
