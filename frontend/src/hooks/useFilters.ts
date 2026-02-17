import { useState } from 'react';

export const useFilters = () => {
  const [filters, setFilters] = useState({});

  const updateFilter = (filterName: string, value: any) => {
    setFilters(prevFilters => ({
      ...prevFilters,
      [filterName]: value,
    }));
  };

  return {
    filters,
    updateFilter,
  };
};
