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
