import { Card, CardContent, Grid2, Typography } from "@mui/material";
import React from "react";
import BarChartComponent from "./BarChartComponent";
import PieChartComponent from "./PieChartComponent";
// import LineChartComponent from "./LineChartComponent";

const Vehicles = ({ statsData }) => {
  const vehiclesDriving = statsData.vehicles.filter(
    (vehicle) => vehicle.isAvailable === false,
  ).length;

  const totalVehicleDistance = statsData.vehicles.reduce(
    (sum, vehicle) => sum + (vehicle.distanceTravelled || 0),
    0,
  );

  const totalTrips = statsData.vehicles.reduce(
    (sum, vehicle) => sum + (vehicle.numberOfTrips || 0),
    0,
  );

  const fuelConsumption = statsData.Vehicles.sum(
    (vehicle) => vehicle.isAvailable === false,
  ).length;

  const vehicleBarChartData = statsData.vehicles.map((vehicle, index) => ({
    name: vehicle.id || `Car ${index + 1}`, // Default name if vehicle.name is missing
    distance: vehicle.distanceTravelled || 0, // Default to 0 if distanceTravelled is missing
  }));

  const vehicleTripsPieData = statsData.vehicles.map((vehicle, index) => ({
    name: vehicle.id || `Car ${index + 1}`, // Default name if vehicle.name is missing
    distance: vehicle.numberOfTrips || 0, // Default to 0 if numberOfTrips is missing
  }));

  const getFuelEfficiency = (speed) => {
    if (speed <= 20) return 5; // km/l for very low speeds
    if (speed <= 60) return 15; // Optimal efficiency
    if (speed <= 100) return 12; // Slightly less efficient
    return 8; // km/l for high speeds
  };

  // Function to calculate fuel consumption
  const calculateTotalFuelConsumption = (vehicles) => {
    return vehicles.reduce((total, vehicle) => {
      const { distanceTravelled, remainingTravelTime, vehicleSpeed } = vehicle;

      // Calculate total distance
      const totalDistance = distanceTravelled + vehicleSpeed * (remainingTravelTime / 60); // Convert time from minutes to hours

      // Get fuel efficiency based on speed
      const fuelEfficiency = getFuelEfficiency(vehicleSpeed);

      // Calculate fuel consumption for this vehicle
      const fuelConsumption = totalDistance / fuelEfficiency;

      // Add this vehicle's fuel consumption to the total
      return total + fuelConsumption;
    }, 0); // Initialize total to 0
  };

  return (
    <Grid2 container spacing={3} padding={3} direction="row" sx={{ height: "100vh" }}>
      {/* Stats Section */}
      <Grid2 size={{ xs: 12, md: 6 }}>
        <Card>
          <CardContent>
            <Typography variant="h5">Vehicles Currently Handled</Typography>
            <Typography variant="h2" color="primary">{vehiclesDriving}</Typography>
          </CardContent>
        </Card>
      </Grid2>
      <Grid2 size={{ xs: 12, md: 6 }}>
        <Card>
          <CardContent>
            <Typography variant="h5">Expected Fuel Consumption</Typography>
            <Typography variant="h2" color="secondary">{calculateTotalFuelConsumption}</Typography>
          </CardContent>
        </Card>
      </Grid2>

      {/* Charts Section */}
      <Grid2 size={{ xs: 12, md: 6 }}>
        <Card>
          <CardContent>
            <Typography variant="h6">
              Distance Driven
            </Typography>

            <BarChartComponent data={vehicleBarChartData} />
          </CardContent>
        </Card>
      </Grid2>
      <Grid2 size={{ xs: 12, md: 6 }}>
        <Card>
          <CardContent>
            <Typography variant="h6">Trips Completed</Typography>

            <PieChartComponent data={vehicleTripsPieData} />
          </CardContent>
        </Card>
      </Grid2>

      {/* Stats Section */}
      <Grid2 size={{ xs: 12, md: 6 }}>
        <Card>
          <CardContent>
            <Typography variant="h5">Total Distance</Typography>
            <Typography variant="h2" color="primary">{totalVehicleDistance}</Typography>
          </CardContent>
        </Card>
      </Grid2>
      <Grid2 size={{ xs: 12, md: 6 }}>
        <Card>
          <CardContent>
            <Typography variant="h5">Total Comissions</Typography>
            <Typography variant="h2" color="secondary">{totalTrips}</Typography>
          </CardContent>
        </Card>
      </Grid2>
    </Grid2>
  );
};

export default Vehicles;
