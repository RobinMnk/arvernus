// import logo from './logo.svg';
// import './App.css';
// import { Box } from '@mui/material';
// import DashboardIcon from '@mui/icons-material/Dashboard';
// import LabelIcon from '@mui/icons-material/Label';
import { createTheme } from "@mui/material/styles";
import axios from "axios";
import React from "react";
import { Admin, Resource } from "react-admin";
import Dashboard from "./Dashboard";
import MyLayout from "./MyLayout";
import Optimization from "./Optimization";
import Vehicles from "./Vehicles";

import DirectionsCarIcon from "@mui/icons-material/DirectionsCar"; // For Vehicles
import SettingsSuggestIcon from "@mui/icons-material/SettingsSuggest"; // For Optimization
import { useEffect, useState } from "react";

const theme = createTheme({
  palette: {
    primary: {
      main: "#1976d2",
    },
    secondary: {
      main: "#D5006D",
    },
    background: {
      default: "#f4f4f4",
      paper: "#ffffff",
    },
    text: {
      primary: "#000000",
      secondary: "#757575",
    },
  },
  typography: {
    fontFamily: "Roboto, Arial, sans-serif",
  },
});

const App = () => {
  const usePolling = (fetchFunction, intervalMs) => {
    const [data, setData] = useState(undefined);

    useEffect(() => {
      const interval = setInterval(async () => {
        const result = await fetchFunction();
        setData(result.data);
      }, intervalMs);

      return () => clearInterval(interval);
    }, [fetchFunction, intervalMs]);

    return data;
  };

  const [scenario_id, set_scenario_id] = useState(undefined);

  const fetchData = async () => {
    if (scenario_id === undefined) {
      return 0;
    }
    try {
      const scenario = await axios.get(
        "http://localhost:3000/api/Scenarios/get_scenario/" + scenario_id,
      );
      return scenario;
    } catch (e) {
      return null;
    }
  };

  const data = usePolling(fetchData, 1000);

  return (
    <Admin
      layout={MyLayout} // Custom layout for sidebar
      dashboard={() => <Dashboard statsData={data} set_scenario_id={set_scenario_id} />} // Dashboard as the first page
      dataProvider={() => Promise.resolve({ data: [] })} // Dummy data provider
      theme={theme}
    >
      <Resource name="Vehicles" list={() => <Vehicles statsData={data} />} icon={DirectionsCarIcon} />
      <Resource
        name="Optimization Criteria"
        list={() => (
          <Optimization
            statsData={data}
          />
        )}
        icon={SettingsSuggestIcon}
      />
    </Admin>
  );
};

export default App;
