import { Button, TextField, Typography } from "@mui/material";
import Box from "@mui/material/Box";
import axios from "axios";
import React, { useState } from "react";
import { AppBar, Layout, Title, UserMenu } from "react-admin";
import { MyMenu } from "./MyMenu";
// import MenuIcon from '@mui/icons-material/Menu';

// const MyAppBar = (props) => (
//     <AppBar {...props} userMenu={<MyUserMenu />} />
//   );

const MyAppBar = (props) => {
  const [button_text, set_button_text] = useState("Launch");
  const [scenario_text, set_scenario_text] = useState("");

  const handleClick = async () => {
    set_button_text("Running");
    props.scenario_id_hook(scenario_text);

    await axios.post(
      "http://localhost:3000/backend/run/" + scenario_text,
    );

    set_button_text("Launch");
    props.scenario_id_hook(undefined);
  };

  const scenarioIdChanged = (event) => {
    set_scenario_text(event.target.value);
  };

  return (
    <AppBar {...props}>
      {/* Align items with flexbox */}
      <Box display="flex" alignItems="center" width="100%">
        {/* Existing title (can be removed if not needed) */}
        <Title />
        {/* Add firm name */}
        <Typography variant="h6" component="div" sx={{ marginLeft: "5px", flexGrow: 2 }}>
          Arvernus
        </Typography>
        <TextField
          id="outlined-basic"
          label="Scenario"
          variant="filled"
          onChange={scenarioIdChanged}
          value={scenario_text}
        />
        <Button variant="outlined" onClick={handleClick}>{button_text}</Button>
        {/* Keep only the user menu, no refresh button */}
        <UserMenu />
      </Box>
    </AppBar>
  );
};

const MyLayout = (props) => (
  <Layout
    {...props}
    menu={MyMenu}
    appBar={() => <MyAppBar scenario_id={props.scenario_id} scenario_id_hook={props.scenario_id_hook} />}
  />
);

// const MyLayout = (props) => (<Layout {...props} menu={MyMenu}/>);
export default MyLayout;
