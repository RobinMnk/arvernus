import React from "react";

import { Bar } from "react-chartjs-2";
import { Chart as ChartJS, BarElement, CategoryScale, LinearScale, Tooltip, Legend } from "chart.js";

// Register the necessary components from Chart.js
ChartJS.register(BarElement, CategoryScale, LinearScale, Tooltip, Legend);


const BarChartComponent = ({ data }) => {
  console.log("BarChart data:", data);
  const chartData = {
    labels: data.map((car) => car.name),
    datasets: [
      {
        label: "Distance (km)",
        data: data.map((car) => car.distance),
        backgroundColor: "rgba(75, 192, 192, 0.6)",
      },
    ],
  };

  const options = {
    responsive: true,
    plugins: {
      legend: { display: true, position: "bottom" },
      title: { display: true, text: "Distance Driven" },
    },
  };

  return <Bar data={chartData} options={options} />;
};

export default BarChartComponent;
