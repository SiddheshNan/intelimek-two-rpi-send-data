import React from "react";

const border = "border border-slate-600";

interface TableProps {
  values: string[];
  timestamp: string[];
  title: string;
  col1: string;
  col2: string;
}

const TableComp: React.FC<TableProps> = ({
  title,
  values,
  timestamp,
  col1,
  col2,
}) => {
  return (
    <div className={`bg-white shadow-md blockHeight p-4 overflow-auto `}>
      <h1 className="text-center text-xl mb-2 font-bold">Table: {title}</h1>
      <table className={`min-w-full border-collapse p-4 ${border}`}>
        <thead>
          <tr>
            <th className={`text-left ${border} px-2 py-2`}>{col1}</th>
            <th className={`text-left ${border} px-2 py-2`}>{col2}</th>
          </tr>
        </thead>
        <tbody className="">
          {values.map((item, index) => (
            <tr key={index}>
              <td className={`text-left ${border} px-2 py-1`}>{item}</td>
              <td className={`text-left ${border} px-2 py-1`}>
                {timestamp[index]}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default TableComp;
