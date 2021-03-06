export const toMonthYearString = (dateValue) => {
  if (!dateValue || !dateValue.trim("")) {
    return "present";
  }

  const [, yearValue, monthValue] = dateValue.match(/^(\d{4})-([01]\d)$/);
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

export const compareNumbers = (a, b) => a - b;

export const compareStatusCodes = (statusCodeA, statusCodeB) => {
  const orderedStatusCodes = [
    "JobAdded",
    "Note",
    "ApplicationSubmitted",
    "ScreeningScheduled",
    "ScreeningCompleted",
    "AssessmentScheduled",
    "AssessmentCompleted",
    "InterviewScheduled",
    "InterviewCompleted",
    "Rejected",
    "OfferMade",
    "OfferAccepted",
    "OfferRejected",
  ];

  if (statusCodeA === statusCodeB) {
    return 0;
  }

  for (const statusCode of orderedStatusCodes) {
    if (statusCode === statusCodeA) {
      return -1;
    } else if (statusCode === statusCodeB) {
      return 1;
    }
  }
};

export const statusCodeToMsg = (statusCode) => {
  const statusCodeToMsgDict = {
    JobAdded: "Job Added",
    Note: "Note",
    ApplicationSubmitted: "Application Submitted",
    ScreeningScheduled: "Screening Scheduled",
    ScreeningCompleted: "Screening Completed",
    AssessmentScheduled: "Assessment Scheduled",
    AssessmentCompleted: "Assessment Completed",
    InterviewScheduled: "Interview Scheduled",
    InterviewCompleted: "Interview Completed",
    Rejected: " Rejected",
    OfferMade: "Offer Made",
    OfferAccepted: "Offer Accepted",
    OfferRejected: "Offer Rejected",
  };
  return statusCodeToMsgDict[statusCode];
};

export const toLocaleDateString = (dateString) =>
  new Date(dateString).toLocaleDateString();

export const extractAdditonalDataFromEvent = (event) => {
  if (event.eventType === "Note") {
    return event.comment;
  } else if (
    ["ScreeningScheduled", "InterviewScheduled"].includes(event.eventType)
  ) {
    return `Scheduled for ${toLocaleDateString(event.eventDate)}.`;
  } else if (["AssessmentScheduled"].includes(event.eventType)) {
    return `Due on ${toLocaleDateString(event.eventDate)}.`;
  }
  return "";
};

export const addressToString = (address) => {
  if (address) {
    return [address.lineOne, address.lineTwo, address.lineThree]
      .filter((x) => x)
      .join(", ");
  } else {
    return "";
  }
};

export function debounce(func, wait, immediate) {
  var timeout;
  return function() {
    var context = this,
      args = arguments;
    var later = function() {
      timeout = null;
      if (!immediate) func.apply(context, args);
    };
    var callNow = immediate && !timeout;
    clearTimeout(timeout);
    timeout = setTimeout(later, wait);
    if (callNow) func.apply(context, args);
  };
}
