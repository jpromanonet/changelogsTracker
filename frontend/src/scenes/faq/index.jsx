import { Box, useTheme } from "@mui/material";
import Header from "../../components/Header";
import Accordion from "@mui/material/Accordion";
import AccordionSummary from "@mui/material/AccordionSummary";
import AccordionDetails from "@mui/material/AccordionDetails";
import Typography from "@mui/material/Typography";
import ExpandMoreIcon from "@mui/icons-material/ExpandMore";
import { tokens } from "../../theme";

const FAQ = () => {
  const theme = useTheme();
  const colors = tokens(theme.palette.mode);
  return (
    <Box m="20px">
      <Header title="FAQ" subtitle="Frequently Asked Questions Page" />

      <Accordion defaultExpanded>
        <AccordionSummary expandIcon={<ExpandMoreIcon />}>
          <Typography color={colors.greenAccent[500]} variant="h5">
            ¿Para que sirve esta app?
          </Typography>
        </AccordionSummary>
        <AccordionDetails>
          <Typography>
            Lee los sitios de changelog de las diferentes integraciones como Mercado Pago, Magento, VTEX, Tienda Nube, etc.
          </Typography>
        </AccordionDetails>
      </Accordion>
      <Accordion defaultExpanded>
        <AccordionSummary expandIcon={<ExpandMoreIcon />}>
          <Typography color={colors.greenAccent[500]} variant="h5">
            ¿Cada cuanto lee los changelogs externos?
          </Typography>
        </AccordionSummary>
        <AccordionDetails>
          <Typography>
            Cada 1 minuto
          </Typography>
        </AccordionDetails>
      </Accordion>
      <Accordion defaultExpanded>
        <AccordionSummary expandIcon={<ExpandMoreIcon />}>
          <Typography color={colors.greenAccent[500]} variant="h5">
            ¿Qué changelogs nos muestra?
          </Typography>
        </AccordionSummary>
        <AccordionDetails>
          <Typography>
            Siempre revisa si existe un nuevo changelog arriba del sitio, y lo suma a la base de datos, sino no encuentra nada, no lo suma.
          </Typography>
        </AccordionDetails>
      </Accordion>
      <Accordion defaultExpanded>
        <AccordionSummary expandIcon={<ExpandMoreIcon />}>
          <Typography color={colors.greenAccent[500]} variant="h5">
            ¿Quién mantiene esta app?
          </Typography>
        </AccordionSummary>
        <AccordionDetails>
          <Typography component="a" href="https://jpromanonet.vercel.app" target="_blank">
            Juan P. Romano
          </Typography>
        </AccordionDetails>
      </Accordion>
    </Box>
  );
};

export default FAQ;
