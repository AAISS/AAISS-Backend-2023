import React from 'react';
import { Checklist } from '@mui/icons-material';
import ListIcon from '@mui/icons-material/List';
import {
  Dialog,
  DialogTitle,
  DialogContent,
  DialogContentText,
  DialogActions,
  Button,
  Divider,
  Stack,
  Chip,
} from '@mui/material';
import PropTypes from 'prop-types';
import { Cost, levelComponentMapping, Presenter } from './item-card';

const Prerequisites = ({ prerequisites }) => (
  <>
    <Stack flexDirection="row" alignItems="center" gap={2}>
      <Checklist fontSize="large" />
      <DialogContentText variant="h6" fontWeight={600}>
        Prerequisites
      </DialogContentText>
    </Stack>
    <DialogContentText>{prerequisites}</DialogContentText>
  </>
);

const Syllabus = ({ syllabus }) => (
  <>
    <Stack flexDirection="row" alignItems="center" gap={2}>
      <ListIcon fontSize="large" />
      <DialogContentText variant="h6" fontWeight={600}>
        Syllabus
      </DialogContentText>
    </Stack>
    <DialogContentText>{syllabus}</DialogContentText>
  </>
);

const MoreInfoModal = ({
  visibility,
  onVisibilityChange,
  title,
  presenterName,
  cost,
  level,
  purchaseState,
  hasProject,
  prerequisites,
  syllabus,
  isFull,
  onClickAddToCart,
  onClickRemoveFromCart,
}) => {
  const handleClickAddToCart = () => {
    onVisibilityChange();
    onClickAddToCart();
  };

  return (
    <Dialog
      onClose={onVisibilityChange}
      open={visibility}
      PaperProps={{
        style: {
          backgroundColor: 'var(--background-color-lighter-20)',
        },
      }}
    >
      <DialogTitle variant="h5">{title}</DialogTitle>
      <DialogContent>
        <Presenter presenterName={presenterName} />
        {levelComponentMapping[level]}
        <Cost cost={cost} />
        <Divider sx={{ my: 2 }} />
        <Prerequisites prerequisites={prerequisites} />
        <Divider sx={{ my: 2 }} />
        <Syllabus syllabus={syllabus} />
        {hasProject && (
          <>
            <Divider sx={{ my: 2 }} />
            <Chip label="Has Project" color="primary" variant="outlined" />
          </>
        )}
      </DialogContent>
      <DialogActions>
        <Button onClick={onVisibilityChange}>Close</Button>
        {purchaseState === 0 ? (
          <Button disabled={isFull} onClick={handleClickAddToCart}>
            Add To Cart
          </Button>
        ) : purchaseState === 1 ? (
          <Button onClick={onClickRemoveFromCart} color="error">
            Remove From Cart
          </Button>
        ) : null}
      </DialogActions>
    </Dialog>
  );
};

MoreInfoModal.propTypes = {
  title: PropTypes.string,
  presenterName: PropTypes.string,
  cost: PropTypes.number,
  level: PropTypes.string,
  isBought: PropTypes.bool,
  purchaseState: PropTypes.number,
  prerequisites: PropTypes.string,
  syllabus: PropTypes.string,
  isFull: PropTypes.bool,
  onClickAddToCart: PropTypes.func,
  onClickRemoveFromCart: PropTypes.func,
};

export default MoreInfoModal;
