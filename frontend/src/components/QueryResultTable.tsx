import { TableHead, TableRow, TableHeader, TableCell, TableBody, Table } from "@/components/ui/table";
import { Data } from "@/types";
import { useState } from 'react';
import { FaChevronLeft, FaChevronRight } from 'react-icons/fa'; // Importation des icônes

export function QueryResultTable({ result }: { result: Data['result'] }) {
    const [currentPage, setCurrentPage] = useState(1);
    const itemsPerPage = 10;

    const totalItems = result.length;
    const totalPages = Math.ceil(totalItems / itemsPerPage);

    const startIndex = (currentPage - 1) * itemsPerPage;
    const endIndex = Math.min(startIndex + itemsPerPage, totalItems);

    const handleNextPage = () => {
        setCurrentPage((prevPage) => Math.min(prevPage + 1, totalPages));
    };

    const handlePreviousPage = () => {
        setCurrentPage((prevPage) => Math.max(prevPage - 1, 1));
    };

    return (
        <div className="flex flex-col gap-2">
            <Table>
                <TableHeader>
                    <TableRow>
                        {Object.keys(result[0]).map((key) => (
                            <TableHead key={key}>{key}</TableHead>
                        ))}
                    </TableRow>
                </TableHeader>
                <TableBody>
                    {result.slice(startIndex, endIndex).map((item, index) => (
                        <TableRow key={startIndex + index}>
                            {Object.values(item).map((value, index) => (
                                <TableCell key={index}>{value}</TableCell>
                            ))}
                        </TableRow>
                    ))}
                </TableBody>
            </Table>
            <div className="flex justify-between items-center">
                <button onClick={handlePreviousPage} disabled={currentPage === 1} className="bg-gray-200 p-2 rounded-full">
                    <FaChevronLeft />
                </button>
                <div>{`Page ${currentPage} of ${totalPages}`}</div>
                <button onClick={handleNextPage} disabled={currentPage === totalPages} className="bg-gray-200 p-2 rounded-full">
                    <FaChevronRight />
                </button>
            </div>
        </div>
    )
}
