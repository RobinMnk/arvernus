import React from 'react';
import { Menu } from 'react-admin';
import PeopleIcon from '@mui/icons-material/People'; // For Customers
// import LabelIcon from '@mui/icons-material/Label';

export const MyMenu = () => (
    <Menu name="Arvernus">
      <Menu.DashboardItem primaryText="Customers" leftIcon={<PeopleIcon/>}/>
 
      <Menu.ResourceItem name="Vehicles" />
      <Menu.ResourceItem name="Optimization Criteria" />
    </Menu>
  );

