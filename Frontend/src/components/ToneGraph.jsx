// src/components/ToneGraph.jsx
import React from "react";
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from "recharts";

const data = [
  { time: "10:00 AM", audio1: 40, audio2: 30 },
  { time: "10:30 AM", audio1: 50, audio2: 25 },
  { time: "11:00 AM", audio1: 35, audio2: 40 },
  { time: "11:30 AM", audio1: 60, audio2: 20 },
  { time: "12:00 PM", audio1: 55, audio2: 25 },
];

const ToneGraph = () => {
  return (
    <div className="tone-graph" style={{ width: "100%", height: 350 }}>
      <h3 style={{ textAlign: "center", marginBottom: "10px", color: "#333" }}>
        Audio Comparison Analysis
      </h3>
      <ResponsiveContainer width="100%" height="100%">
        <LineChart data={data} margin={{ top: 10, right: 30, left: 20, bottom: 10 }}>
          <CartesianGrid strokeDasharray="3 3" stroke="#ccc" />
          <XAxis dataKey="time" tick={{ fontSize: 12 }} />
          <YAxis domain={[0, 100]} tick={{ fontSize: 12 }} />
          <Tooltip
            contentStyle={{ backgroundColor: "#fff", borderRadius: "5px" }}
            labelStyle={{ fontWeight: "bold" }}
          />
          <Legend verticalAlign="top" align="right" />
          <Line type="monotone" dataKey="audio1" stroke="#4CAF50" strokeWidth={2} dot={{ r: 3 }} />
          <Line type="monotone" dataKey="audio2" stroke="#2196F3" strokeWidth={2} dot={{ r: 3 }} />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
};

export default ToneGraph;
