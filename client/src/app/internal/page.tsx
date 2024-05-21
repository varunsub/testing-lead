"use client";
import { useEffect, useState } from "react";
import axios from "axios";
import { useRouter } from "next/navigation";
import styles from './internal.module.css';
import Pagination from '../../components/Pagination';

interface Lead {
  id: string;
  first_name: string;
  last_name: string;
  email: string;
  state: string;
}
export default function Internal() {
  const [leads, setLeads] = useState<Lead[]>([]);
  const [message, setMessage] = useState<string>('');
  const [total, setTotal] = useState<number>(0);
  const [currentPage, setCurrentPage] = useState<number>(1);
  const [limit] = useState<number>(10); // Number of items per page
  const router = useRouter();

  useEffect(() => {
    const fetchLeads = async (page: number, limit: number) => {
      try {
        const skip = (page - 1) * limit;
        const response = await axios.get(`${process.env.NEXT_PUBLIC_API_URL}/leads/`, {
          params: { skip, limit },
          withCredentials: true,
        });
        setLeads(response.data.leads);
        setTotal(response.data.total);
      } catch (error: any) {
        setMessage('Failed to fetch leads.');
        if (error.response?.status === 401) {
          router.push('/login');
        }
      }
    };

    fetchLeads(currentPage, limit);
  }, [currentPage, limit, router]);

  const updateLeadState = async (leadId: string) => {
    try {
      await axios.patch(`${process.env.NEXT_PUBLIC_API_URL}/leads/${leadId}/`, {
        state: "REACHED_OUT",
      }, {
        withCredentials: true,
      });
      setLeads(leads.map(lead => 
        lead.id === leadId ? {...lead, state: "REACHED_OUT"} : lead
      ));
      setMessage(`Lead ${leadId} updated successfully.`);
    } catch (error: any) {
      setMessage('Failed to update lead state.');
      if (error.response?.status === 401) {
        router.push('/login');
      }
    }
  };

  return (
    <div className={styles.container}>
      <h1>Leads List</h1>
      {message && <p className={styles.message}>{message}</p>}
      <table className={styles.table}>
        <thead>
          <tr>
            <th>First Name</th>
            <th>Last Name</th>
            <th>Email</th>
            <th>State</th>
            <th>Action</th>
          </tr>
        </thead>
        <tbody>
          {leads.map(lead => (
            <tr key={lead.id}>
              <td>{lead.first_name}</td>
              <td>{lead.last_name}</td>
              <td>{lead.email}</td>
              <td>{lead.state}</td>
              <td>
                {lead.state !== "REACHED_OUT" && (
                  <button 
                    onClick={() => updateLeadState(lead.id)} 
                    className={styles.button}
                  >
                    Mark as Reached Out
                  </button>
                )}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
      <Pagination
        total={total}
        limit={limit}
        currentPage={currentPage}
        setPage={setCurrentPage}
      />
    </div>
  );
}