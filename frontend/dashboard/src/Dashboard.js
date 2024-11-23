import { Card, CardContent, Grid2, Typography } from "@mui/material";
import React from "react";
// import BarChartComponent from "./BarChartComponent";
// import PieChartComponent from "./PieChartComponent";
import { useEffect, useState } from "react";
import LineChartComponent from "./LineChartComponent";

const Dashboard = ({ statsData }) => {

// Get current time in HH:mm format
const timestamp = new Date().toLocaleTimeString([], {
    hour: "2-digit",
    minute: "2-digit",
    second: "2-digit",
});

const [chartData, setChartData] = useState([]);

  useEffect(() => {
    const interval = setInterval(() => {
      if (!statsData?.customers) return;

      // Calculate the number of customers awaiting service
      const customersAwaitingService = statsData.customers.filter(
        (customer) => customer.awaitingService === true,
      ).length;

      
      const updatedData = [...chartData, { timestamp, customers: customersAwaitingService }];

      // Keep only the latest 10 data points (optional)
      if (updatedData.length > 10) {
        updatedData.shift(); // Remove the oldest entry
      }

      // Update chart data
      setChartData(updatedData);
    }, 1000);

    return () => clearInterval(interval);
  }, [statsData]);


  const customersAwaitingService = !statsData?.customers ? 0 : statsData.customers.filter(
    (customer) => customer.awaitingService === true,
  ).length;

  const customersDone = !statsData?.customers ? 0 : statsData.customers.filter(
    (customer) => customer.awaitingService === false,
  ).length;

  return (
    <Grid2 container spacing={3} padding={3}>
      {/* Stats Section */}
      <Grid2 size={6}>
        <Card>
          <CardContent>
            <Typography variant="h5">Customers Waiting</Typography>
            <Typography variant="h2" color="primary">{customersAwaitingService}</Typography>
          </CardContent>
        </Card>
      </Grid2>
      <Grid2 size={6}>
        <Card>
          <CardContent>
            <Typography variant="h5">Customers Delivered</Typography>
            <Typography variant="h2" color="secondary">{customersDone}</Typography>
          </CardContent>
        </Card>
      </Grid2>

      <Grid2 size={12}>
        <Card>
          <CardContent>
            <Typography variant="h6">Real-Time Customer Count in Cars</Typography>

            <LineChartComponent data={chartData} />
          </CardContent>
        </Card>
      </Grid2>
    </Grid2>
  );
};

export default Dashboard;
