export const renderMonth = (dateValue) => {
  if (!dateValue.trim("")) {
    return "present";
  }

  var monthValue, yearValue;
  [, yearValue, monthValue] = dateValue.match(/^(\d{4})-([01]\d)$/);
  const numToAbbreviatedMonth = {
    "01": "Jan.",
    "02": "Feb.",
    "03": "Mar.",
    "04": "Apr.",
    "05": "May",
    "06": "June",
    "07": "July",
    "08": "Aug.",
    "09": "Sep.",
    "10": "Oct.",
    "11": "Nov.",
    "12": "Dec.",
  };
  return `${numToAbbreviatedMonth[monthValue]} ${yearValue}`;
};

export const statusCodeToMsg = (statusCode) => {
  const statusCodeToMsgDict = {
    "JobAdded": "Job Added",
    "Note": "Note",
    "ApplicationSubmitted": "Application Submitted",
    "ScreeningScheduled": "Screening Scheduled",
    "ScreeningCompleted": "Screening Completed",
    "AssessmentScheduled": "Assessment Scheduled",
    "AssessmentCompleted": "Assessment Completed",
    "InterviewScheduled": "Interview Scheduled",
    "InterviewCompleted": "Interview Completed",
    "Rejected":" Rejected",
    "OfferMade": "Offer Made",
    "OfferAccepted": "Offer Accepted",
    "OfferRejected": "Offer Rejected",
  }
  return statusCodeToMsgDict[statusCode]
}