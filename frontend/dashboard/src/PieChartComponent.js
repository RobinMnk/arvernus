import {
  ArcElement,
  CategoryScale,
  Chart as ChartJS,
  Legend,
  LinearScale,
  LineElement,
  PointElement,
  Tooltip,
} from "chart.js";
import React from "react";
import { Pie } from "react-chartjs-2";

// Register required chart.js components
ChartJS.register(
  ArcElement,
  Tooltip,
  Legend,
  LineElement,
  CategoryScale,
  LinearScale,
  PointElement,
);

const PieChartComponent = ({ data }) => {
  const chartData = {
    labels: !data ? 0 : data.map((car) => car.name),
    datasets: [
      {
        label: "Trips",
        data: !data ? 0 : data.map((car) => car.trips),
        backgroundColor: ["#ff6384", "#36a2eb", "#ffce56", "#4bc0c0", "#9966ff"],
      },
    ],
  };

  const options = {
    responsive: true,
    plugins: {
      legend: { position: "right" },
      title: { display: true, text: "Trips Completed" },
    },
  };

  return <Pie data={chartData} options={options} />;
};

export default PieChartComponent;
