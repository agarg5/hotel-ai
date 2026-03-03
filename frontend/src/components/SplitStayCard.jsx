export default function SplitStayCard({ segments }) {
  return (
    <div className="split-stay-card">
      <h3>Split Stay</h3>
      {segments.map((seg, i) => (
        <div className="segment" key={i}>
          <strong>{seg.room}</strong> — {seg.check_in} to {seg.check_out} (
          {seg.nights} night{seg.nights !== 1 ? "s" : ""})
        </div>
      ))}
    </div>
  );
}
