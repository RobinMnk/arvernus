import React from "react";
import { Grid2, Card, CardContent, Typography } from "@mui/material";
import BarChartComponent from "./BarChartComponent";
import PieChartComponent from "./PieChartComponent";
import LineChartComponent from "./LineChartComponent";


const Optimization = ({ statsData, barChartData, pieChartData, lineChartData }) => {
  return (
    <Grid2 container spacing={3} padding={3}>
      {/* Stats Section */}
      <Grid2 size={{xs:12, md:6}}>
      <Card>
      <CardContent>
            <Typography variant="h5">Customers Satisfcation</Typography>

            </CardContent>
            </Card>
      </Grid2>
      <Grid2 size={{xs:12, md:6}}>
        <Card >
          <CardContent>
            <Typography variant="h5">Environmental Footprint</Typography>
          </CardContent>
        </Card>
      </Grid2>
    </Grid2>
  );
};

export default Optimization;
