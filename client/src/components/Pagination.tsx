"use client"
import styles from './Pagination.module.css'; // Assuming you have a CSS module file

interface PaginationProps {
  total: number;
  limit: number;
  currentPage: number;
  setPage: (page: number) => void;
}

const Pagination: React.FC<PaginationProps> = ({ total, limit, currentPage, setPage }) => {
  const totalPages = Math.ceil(total / limit);
  return (
    <div className={styles.pagination}>
      <button onClick={() => setPage(currentPage - 1)} disabled={currentPage === 1}>
        Previous
      </button>
      {Array.from({ length: totalPages }, (_, index) => (
        <button
          key={index + 1}
          onClick={() => setPage(index + 1)}
          className={currentPage === index + 1 ? styles.active : ''}
          disabled={currentPage === index + 1}
        >
          {index + 1}
        </button>
      ))}
      <button onClick={() => setPage(currentPage + 1)} disabled={currentPage === totalPages}>
        Next
      </button>
    </div>
  );
};
export default Pagination;