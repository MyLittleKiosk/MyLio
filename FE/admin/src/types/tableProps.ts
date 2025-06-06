export interface Column<T> {
  header: string;
  accessor: keyof T;
  className?: string;
}

export interface TableProps<T> {
  title: string;
  description: string;
  columns: Column<T>[];
  data: T[];
  className?: string;
  onEdit?: (row: T) => void;
  onDelete?: (row: T) => void;
  onView?: (row: T) => void;
}
