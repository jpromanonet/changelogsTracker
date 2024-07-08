// src/scenes/dashboard/Dashboard.js
import React, { useEffect, useState } from 'react';
import { Box, Typography, Select, MenuItem, useTheme } from "@mui/material";
import { tokens } from "../../theme";
import Header from "../../components/Header";
import changelogService from '../../services/changelogService';

const Dashboard = () => {
  const theme = useTheme();
  const colors = tokens(theme.palette.mode);
  const [changelogs, setChangelogs] = useState([]);
  const [filteredChangelogs, setFilteredChangelogs] = useState([]);
  const [selectedSite, setSelectedSite] = useState('All');

  useEffect(() => {
    const fetchChangelogs = async () => {
      try {
        const data = await changelogService.getChangelogs();
        setChangelogs(data);
        setFilteredChangelogs(data);
      } catch (error) {
        console.error('Error fetching changelogs:', error);
      }
    };

    fetchChangelogs();
  }, []);

  useEffect(() => {
    if (selectedSite === 'All') {
      setFilteredChangelogs(changelogs);
    } else {
      setFilteredChangelogs(changelogs.filter(changelog => changelog.site === selectedSite));
    }
  }, [selectedSite, changelogs]);

  const handleSiteChange = (event) => {
    setSelectedSite(event.target.value);
  };

  return (
    <Box m="20px">
      {/* HEADER */}
      <Box display="flex" flexDirection="column" justifyContent="space-between" alignItems="left">
        <Header title="Ultimos changelogs trackeados" />
        <Select
          value={selectedSite}
          onChange={handleSiteChange}
          displayEmpty
          inputProps={{ 'aria-label': 'Without label' }}
          style={{ color: colors.grey[100], backgroundColor: colors.primary[400], marginTop: '20px' }}
        >
          <MenuItem value="All">Todos</MenuItem>
          <MenuItem value="Mercado Pago">Mercado Pago</MenuItem>
          <MenuItem value="VTEX">VTEX</MenuItem>
          {/* Add more sites as needed */}
        </Select>
      </Box>
      <br/>
      {/* GRID & CHARTS */}
      <Box
        display="grid"
        gridAutoRows="100%"
        gap="20px"
      >

        {/* ROW 2 */}
        <Box
          gridColumn="span 12"
          backgroundColor={colors.primary[400]}
          overflow="auto"
        >
          <Box
            display="flex"
            justifyContent="space-between"
            alignItems="center"
            borderBottom={`4px solid ${colors.primary[500]}`}
            colors={colors.grey[100]}
            p="15px"
          >
            <Typography color={colors.grey[100]} variant="h5" fontWeight="600">
              Cambios recientes
            </Typography>
          </Box>
          {filteredChangelogs.map((changelog) => (
            <Box
              key={changelog.id}
              display="flex"
              justifyContent="space-between"
              alignItems="center"
              borderBottom={`4px solid ${colors.primary[500]}`}
              p="15px"
            >
              <Box>
                <Typography
                  color={colors.redAccent[400]}
                  variant="h6"
                  fontWeight="500"
                  style={{ marginBottom: '8px' }}
                >
                  {changelog.site}
                </Typography>
                <br />
                <Typography
                  color={colors.greenAccent[500]}
                  variant="h5"
                  fontWeight="600"
                >
                  {changelog.title}
                </Typography>
                <Box color={colors.grey[100]}>
                  {new Date(changelog.date).toLocaleDateString()}
                </Box>
                <br />
                <Typography color={colors.grey[100]}>
                  {changelog.content}
                </Typography>
              </Box>
            </Box>
          ))}
        </Box>
      </Box>
    </Box>
  );
};

export default Dashboard;