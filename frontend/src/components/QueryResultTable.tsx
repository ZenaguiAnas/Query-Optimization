import {TableHead, TableRow, TableHeader, TableCell, TableBody, Table} from "@/components/ui/table"
import {Data} from "@/types";


export function QueryResultTable({result}: { result: Data['result'] }) {
    console.log(result);

    return (
        <Table>
            <TableHeader>
                <TableRow>
                    {Object.keys(result[0]).map((key) => (
                        <TableHead key={key}>{key}</TableHead>
                    ))}
                    <TableHead className="w-12"/>
                </TableRow>
            </TableHeader>
            <TableBody>
                {result.map((item, index) => (
                    <TableRow key={index}>
                        {Object.values(item).map((value, index) => (
                            <TableCell key={index}>{value}</TableCell>
                        ))}
                    </TableRow>
                ))}
            </TableBody>
        </Table>
    )
}
