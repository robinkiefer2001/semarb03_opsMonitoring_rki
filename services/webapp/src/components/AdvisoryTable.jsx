import React from "react";

export default function AdvisoryTable({
  title,
  rows,
  columns,
  onRowClick,
  rowKey = "id",
  selectedRowKey = "",
}) {
  return (
    <section className="panel">
      <h2>{title}</h2>
      <p className="hint-text">Klick auf eine Zeile fuer Detailansicht.</p>
      <div className="table-wrapper">
        <table>
          <thead>
            <tr>
              {columns.map((column) => (
                <th key={column.key}>{column.label}</th>
              ))}
            </tr>
          </thead>
          <tbody>
            {rows.length === 0 ? (
              <tr>
                <td colSpan={columns.length}>Keine Daten verfuegbar</td>
              </tr>
            ) : (
              rows.map((row, idx) => (
                <tr
                  key={`${row[rowKey] ?? idx}`}
                  className={`clickable-row ${selectedRowKey && row[rowKey] === selectedRowKey ? "active" : ""}`}
                  onClick={() => onRowClick && onRowClick(row)}
                >
                  {columns.map((column) => (
                    <td key={column.key}>{Array.isArray(row[column.key]) ? row[column.key].join(", ") : row[column.key] ?? "-"}</td>
                  ))}
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>
    </section>
  );
}
