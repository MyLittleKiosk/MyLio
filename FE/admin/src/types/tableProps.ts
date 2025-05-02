interface Column<T> {
  header: string;
  accessor: keyof T;
  className?: string;
}

interface TableProps<T> {
  title: string;
  description: string;
  columns: Column<T>[];
  data: T[];
  className?: string;
}

export type { Column, TableProps };
