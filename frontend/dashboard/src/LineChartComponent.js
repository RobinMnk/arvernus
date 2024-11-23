import React from "react";
import {
  Chart as ChartJS,
  ArcElement,
  Tooltip,
  Legend,
  LineElement,
  CategoryScale,
  LinearScale,
  PointElement,
} from 'chart.js';
import { Line } from "react-chartjs-2";

// Register required chart.js components
ChartJS.register(
  ArcElement,
  Tooltip,
  Legend,
  LineElement,
  CategoryScale,
  LinearScale,
  PointElement
);


const LineChartComponent = ({ data }) => {
  const chartData = {
    labels: data.map((record) => record.timestamp),
    datasets: [
      {
        label: "Customers in Cars",
        data: data.map((record) => record.customers),
        borderColor: "#42a5f5",
        fill: true,
        backgroundColor: "rgba(66, 165, 245, 0.2)",
      },
    ],
  };

  const options = {
    responsive: true,
    plugins: {
      legend: { display: true, position: "bottom" },
      title: { display: true, text: "Real-Time Customer Count in Cars" },
    },
    scales: {
      x: { display: true, title: { display: true, text: "Time" } },
      y: { display: true, title: { display: true, text: "Customers" } },
    },
  };

  return <Line data={chartData} options={options} />;
};

export default LineChartComponent;
