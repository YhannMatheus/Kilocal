import { api } from "./api";
import { BioStatusType, GraphPoint } from "@/types/bodyAssessment.types";

class BodyAssessmentService {
    async getGraphData(type: BioStatusType): Promise<GraphPoint[]> {
        const response = await api.get<GraphPoint[]>(`/body-assessment/graph/${type}`);
        return response.data;
    }
}

export const bodyAssessmentService = new BodyAssessmentService();