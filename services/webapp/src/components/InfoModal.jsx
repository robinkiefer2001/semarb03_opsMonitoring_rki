import React from "react";

export default function InfoModal({ open, title, subtitle, onClose, children }) {
  if (!open) {
    return null;
  }

  return (
    <div className="modal-backdrop" onClick={onClose}>
      <section className="modal-window" onClick={(event) => event.stopPropagation()}>
        <header className="modal-header">
          <div>
            <h3>{title}</h3>
            {subtitle && <p>{subtitle}</p>}
          </div>
          <button type="button" className="modal-close" onClick={onClose}>
            Schliessen
          </button>
        </header>
        <div className="modal-content">{children}</div>
      </section>
    </div>
  );
}
