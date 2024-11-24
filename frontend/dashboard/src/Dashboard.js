import { Card, CardContent, Grid2 } from "@mui/material";
import React from "react";
// import BarChartComponent from "./BarChartComponent";
// import PieChartComponent from "./PieChartComponent";
import { Button, TextField, Typography } from "@mui/material";
import axios from "axios";
import { useEffect, useState } from "react";
import LineChartComponent from "./LineChartComponent";

const Dashboard = ({ statsData, set_scenario_id }) => {
  // Get current time in HH:mm format
  const timestamp = new Date().toLocaleTimeString([], {
    hour: "2-digit",
    minute: "2-digit",
    second: "2-digit",
  });

  const [chartData, setChartData] = useState([]);

  useEffect(() => {
    if (!statsData?.customers) return;

    // Calculate the number of customers awaiting service
    const customersAwaitingService = statsData.customers.filter(
      (customer) => customer.awaitingService === true,
    ).length;

    console.log("Before " + JSON.stringify(chartData));
    const updatedData = [...chartData, { timestamp, customers: customersAwaitingService }];
    // const updatedData = chartData;
    // updatedData.push({ timestamp, customers: customersAwaitingService });
    console.log("After " + JSON.stringify(updatedData));

    // // Keep only the latest 10 data points (optional)
    // if (updatedData.length > 10) {
    //   updatedData.shift(); // Remove the oldest entry
    // }

    // Update chart data
    setChartData(updatedData);
  }, [statsData]);

  const customersAwaitingService = !statsData?.customers ? 0 : statsData.customers.filter(
    (customer) => customer.awaitingService === true,
  ).length;

  const customersDone = !statsData?.customers ? 0 : statsData.customers.filter(
    (customer) => customer.awaitingService === false,
  ).length;

  const [button_text, set_button_text] = useState("Launch");
  const [scenario_text, set_scenario_text] = useState("");

  const handleClick = async () => {
    set_button_text("Running");
    set_scenario_id(scenario_text);

    await axios.post(
      "http://localhost:3000/backend/run/" + scenario_text,
    );

    set_button_text("Launch");
    set_scenario_id(undefined);
  };

  const scenarioIdChanged = async (event) => {
    set_scenario_text(event.target.value);
  };

  return (
    <Grid2 container spacing={3} padding={3}>
      <TextField
        id="outlined-basic"
        label="Scenario"
        variant="filled"
        onChange={scenarioIdChanged}
        value={scenario_text}
      />
      <Button variant="outlined" onClick={handleClick}>{button_text}</Button>

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
