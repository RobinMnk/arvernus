// import logo from './logo.svg';
// import './App.css';
// import { Box } from '@mui/material';
// import DashboardIcon from '@mui/icons-material/Dashboard';
// import LabelIcon from '@mui/icons-material/Label';
// import axios from "axios";
import React from "react";
import { createTheme } from "@mui/material/styles";
import Dashboard from "./Dashboard";
import Vehicles from "./Vehicles";
import Optimization from "./Optimization";
import { Admin, Resource } from 'react-admin';
import MyLayout from './MyLayout';

import { useState, useEffect } from "react";
import DirectionsCarIcon from '@mui/icons-material/DirectionsCar'; // For Vehicles
import SettingsSuggestIcon from '@mui/icons-material/SettingsSuggest'; // For Optimization

const theme = createTheme({
  palette: {
    primary: {
      main: '#1976d2',
    },
    secondary: {
      main: '#D5006D',
    },
    background: {
      default: '#f4f4f4',
      paper: '#ffffff',
    },
    text: {
      primary: '#000000',
      secondary: '#757575',
    },
  },
  typography: {
    fontFamily: 'Roboto, Arial, sans-serif',
  },
});


const App = () =>  {


const usePolling = (fetchFunction, intervalMs) => {
  const [data, setData] = useState(null);

  useEffect(() => {
    
    const interval = setInterval(async () => {
      const result = await fetchFunction();
      setData(result);
    }, intervalMs);

    return () => clearInterval(interval);
  }, [fetchFunction, intervalMs]);

  return data;
};

const fetchData = async () => {
  const scenario = await fetch("http://localhost:8090/Scenarios/get_scenario/"); 
  const scenarioData = await scenario.json();
  return scenarioData;
};

const data = usePolling(fetchData, 1000);
  
  return(
    <Admin
      layout={MyLayout} // Custom layout for sidebar
      dashboard={  () => <Dashboard
        statsData={data}
      />} // Dashboard as the first page

      dataProvider={() => Promise.resolve({ data: [] })} // Dummy data provider
      theme={theme}
    >
          <Resource name="Vehicles" list={() =>  <Vehicles  statsData={data}
  />} icon={DirectionsCarIcon}/>
          <Resource name="Optimization Criteria" list={() => <Optimization
    statsData={data}
  />} icon={SettingsSuggestIcon}/>
    </Admin>
  );
}

export default App;

