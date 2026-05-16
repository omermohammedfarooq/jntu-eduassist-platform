"""JNTUH Syllabus Service - Direct PDF downloads."""

from typing import Dict, List, Optional

# Comprehensive syllabus PDF mapping
SYLLABUS_PDF_MAP = {
    "btech": {
        "r22": {
            "1": {
                "common": {
                    "name": "Common (All Branches)",
                    "url": "https://studentservices.jntuh.ac.in/oss/resources/files/SYLLABUS/1.B.Tech/1.R22/1.B.Tech I Year R22 Syllabus/R22 B.Tech. I Year Syllabus.pdf"
                },
                "cse": {
                    "name": "CSE (Computer Science and Engineering)",
                    "url": "https://studentservices.jntuh.ac.in/oss/resources/files/SYLLABUS/1.B.Tech/1.R22/1.B.Tech I Year R22 Syllabus/R22 B.Tech. CSE I Year Syllabus.pdf"
                },
                "cse_aiml": {
                    "name": "CSE (AI & ML)",
                    "url": "https://studentservices.jntuh.ac.in/oss/resources/files/SYLLABUS/1.B.Tech/1.R22/1.B.Tech I Year R22 Syllabus/R22 B.Tech. CSE (AIML) I Year Syllabus.pdf"
                },
                "cse_ds": {
                    "name": "CSE (Data Science)",
                    "url": "https://studentservices.jntuh.ac.in/oss/resources/files/SYLLABUS/1.B.Tech/1.R22/1.B.Tech I Year R22 Syllabus/R22 B.Tech. CSE (Data Science) I Year Syllabus.pdf"
                },
                "cse_cs": {
                    "name": "CSE (Cyber Security)",
                    "url": "https://studentservices.jntuh.ac.in/oss/resources/files/SYLLABUS/1.B.Tech/1.R22/1.B.Tech I Year R22 Syllabus/R22 B.Tech. CSE (Cyber Security) I Year Syllabus.pdf"
                },
                "cse_iot": {
                    "name": "CSE (IoT)",
                    "url": "https://studentservices.jntuh.ac.in/oss/resources/files/SYLLABUS/1.B.Tech/1.R22/1.B.Tech I Year R22 Syllabus/R22 B.Tech. CSE (IOT) I Year Syllabus.pdf"
                },
                "cse_networks": {
                    "name": "CSE (Networks)",
                    "url": "https://studentservices.jntuh.ac.in/oss/resources/files/SYLLABUS/1.B.Tech/1.R22/1.B.Tech I Year R22 Syllabus/R22 B.Tech. CSE (Networks) I Year Syllabus.pdf"
                },
                "it": {
                    "name": "IT (Information Technology)",
                    "url": "https://studentservices.jntuh.ac.in/oss/resources/files/SYLLABUS/1.B.Tech/1.R22/1.B.Tech I Year R22 Syllabus/R22 B.Tech. CSIT I Year Syllabus.pdf"
                },
                "ai_ds": {
                    "name": "AI & DS (Artificial Intelligence and Data Science)",
                    "url": "https://studentservices.jntuh.ac.in/oss/resources/files/SYLLABUS/1.B.Tech/1.R22/1.B.Tech I Year R22 Syllabus/R22 B.Tech. AI&DS I Year Syllabus.pdf"
                },
                "ai_ml": {
                    "name": "AI & ML (Artificial Intelligence and Machine Learning)",
                    "url": "https://studentservices.jntuh.ac.in/oss/resources/files/SYLLABUS/1.B.Tech/1.R22/1.B.Tech I Year R22 Syllabus/R22 B.Tech. AI&ML I Year Syllabus.pdf"
                },
                "csbs": {
                    "name": "CSBS (Computer Science and Business Systems)",
                    "url": "https://studentservices.jntuh.ac.in/oss/resources/files/SYLLABUS/1.B.Tech/1.R22/1.B.Tech I Year R22 Syllabus/R22 B.Tech. CSBS I Year Syllabus.pdf"
                },
                "csd": {
                    "name": "CSD (Computer Science and Design)",
                    "url": "https://studentservices.jntuh.ac.in/oss/resources/files/SYLLABUS/1.B.Tech/1.R22/1.B.Tech I Year R22 Syllabus/R22 B.Tech. CSD I Year Syllabus.pdf"
                },
                "ce_se": {
                    "name": "CE (Software Engineering)",
                    "url": "https://studentservices.jntuh.ac.in/oss/resources/files/SYLLABUS/1.B.Tech/1.R22/1.B.Tech I Year R22 Syllabus/R22 B.Tech. CE (Software Engineering) I Year Syllabus.pdf"
                },
                "ece": {
                    "name": "ECE (Electronics and Communication Engineering)",
                    "url": "https://studentservices.jntuh.ac.in/oss/resources/files/SYLLABUS/1.B.Tech/1.R22/1.B.Tech I Year R22 Syllabus/R22 B.Tech. ECE I Year Syllabus.pdf"
                },
                "eee": {
                    "name": "EEE (Electrical and Electronics Engineering)",
                    "url": "https://studentservices.jntuh.ac.in/oss/resources/files/SYLLABUS/1.B.Tech/1.R22/1.B.Tech I Year R22 Syllabus/R22 B.Tech. EEE I Year Syllabus.pdf"
                },
                "mech": {
                    "name": "MECH (Mechanical Engineering)",
                    "url": "https://studentservices.jntuh.ac.in/oss/resources/files/SYLLABUS/1.B.Tech/1.R22/1.B.Tech I Year R22 Syllabus/R22 B.Tech. MECH I Year Syllabus.pdf"
                },
                "civil": {
                    "name": "CIVIL (Civil Engineering)",
                    "url": "https://studentservices.jntuh.ac.in/oss/resources/files/SYLLABUS/1.B.Tech/1.R22/1.B.Tech I Year R22 Syllabus/R22 B.Tech. CIVIL ENGG. I Year Syllabus.pdf"
                }
            },
            "2": {
                "cse": {
                    "name": "CSE (Computer Science and Engineering)",
                    "url": "https://studentservices.jntuh.ac.in/oss/resources/files/SYLLABUS/1.B.Tech/1.R22/2.B.Tech II Year R22 Syllabus/R22 B.Tech. CSE I and II Year Syllabus.pdf"
                },
                "cse_aiml": {
                    "name": "CSE (AI & ML)",
                    "url": "https://studentservices.jntuh.ac.in/oss/resources/files/SYLLABUS/1.B.Tech/1.R22/2.B.Tech II Year R22 Syllabus/R22 B.Tech. CSE (AI & ML) I and II Year Syllabus.pdf"
                },
                "cse_ds": {
                    "name": "CSE (Data Science)",
                    "url": "https://studentservices.jntuh.ac.in/oss/resources/files/SYLLABUS/1.B.Tech/1.R22/2.B.Tech II Year R22 Syllabus/R22 B.Tech. CSE (Data Science) I and II Year Syllabus.pdf"
                },
                "cse_cs": {
                    "name": "CSE (Cyber Security)",
                    "url": "https://studentservices.jntuh.ac.in/oss/resources/files/SYLLABUS/1.B.Tech/1.R22/2.B.Tech II Year R22 Syllabus/R22 B.Tech. CSE (Cyber Security) I and II Year Syllabus.pdf"
                },
                "cse_iot": {
                    "name": "CSE (IoT)",
                    "url": "https://studentservices.jntuh.ac.in/oss/resources/files/SYLLABUS/1.B.Tech/1.R22/2.B.Tech II Year R22 Syllabus/R22 B.Tech. CSE (IOT) I and II Year Syllabus.pdf"
                },
                "cse_networks": {
                    "name": "CSE (Networks)",
                    "url": "https://studentservices.jntuh.ac.in/oss/resources/files/SYLLABUS/1.B.Tech/1.R22/2.B.Tech II Year R22 Syllabus/R22 B.Tech. CSE (Networks) I and II Year Syllabus.pdf"
                },
                "it": {
                    "name": "IT (Information Technology)",
                    "url": "https://studentservices.jntuh.ac.in/oss/resources/files/SYLLABUS/1.B.Tech/1.R22/2.B.Tech II Year R22 Syllabus/R22 B.Tech. CSIT I and II Year Syllabus.pdf"
                },
                "ai_ds": {
                    "name": "AI & DS (Artificial Intelligence and Data Science)",
                    "url": "https://studentservices.jntuh.ac.in/oss/resources/files/SYLLABUS/1.B.Tech/1.R22/2.B.Tech II Year R22 Syllabus/R22 B.Tech. AI & DS I and II Year Syllabus.pdf"
                },
                "ai_ml": {
                    "name": "AI & ML (Artificial Intelligence and Machine Learning)",
                    "url": "https://studentservices.jntuh.ac.in/oss/resources/files/SYLLABUS/1.B.Tech/1.R22/2.B.Tech II Year R22 Syllabus/R22 B.Tech. AI & ML I and II Year Syllabus.pdf"
                },
                "csbs": {
                    "name": "CSBS (Computer Science and Business Systems)",
                    "url": "https://studentservices.jntuh.ac.in/oss/resources/files/SYLLABUS/1.B.Tech/1.R22/2.B.Tech II Year R22 Syllabus/R22 B.Tech. CSBS Course Structure, I & II Year Syllabus.pdf"
                },
                "csd": {
                    "name": "CSD (Computer Science and Design)",
                    "url": "https://studentservices.jntuh.ac.in/oss/resources/files/SYLLABUS/1.B.Tech/1.R22/2.B.Tech II Year R22 Syllabus/R22 B.Tech. CSD Course Structure, I & II Year Syllabus.pdf"
                },
                "ce_se": {
                    "name": "CE (Software Engineering)",
                    "url": "https://studentservices.jntuh.ac.in/oss/resources/files/SYLLABUS/1.B.Tech/1.R22/2.B.Tech II Year R22 Syllabus/R22 B.Tech. CE (Software Engineering) I and II Year Syllabus.pdf"
                },
                "ece": {
                    "name": "ECE (Electronics and Communication Engineering)",
                    "url": "https://studentservices.jntuh.ac.in/oss/resources/files/SYLLABUS/1.B.Tech/1.R22/2.B.Tech II Year R22 Syllabus/R22 B.Tech. ECE I and II Year Syllabus.pdf"
                },
                "eee": {
                    "name": "EEE (Electrical and Electronics Engineering)",
                    "url": "https://studentservices.jntuh.ac.in/oss/resources/files/SYLLABUS/1.B.Tech/1.R22/2.B.Tech II Year R22 Syllabus/R22 B.Tech. EEE I and II Year Syllabus.pdf"
                },
                "mech": {
                    "name": "MECH (Mechanical Engineering)",
                    "url": "https://studentservices.jntuh.ac.in/oss/resources/files/SYLLABUS/1.B.Tech/1.R22/2.B.Tech II Year R22 Syllabus/R22 B.Tech. MECH I and II Year Syllabus.pdf"
                },
                "civil": {
                    "name": "CIVIL (Civil Engineering)",
                    "url": "https://studentservices.jntuh.ac.in/oss/resources/files/SYLLABUS/1.B.Tech/1.R22/2.B.Tech II Year R22 Syllabus/R22 B.Tech. CIVIL ENGG. I & II Year Syllabus.pdf"
                }
            }
        },
        "r18": {
            "1": {
                "common_cse": {
                    "name": "Common (CSE, ECE, ETE, EIE, ECM, ICE, IT, BME)",
                    "url": "https://studentservices.jntuh.ac.in/oss/resources/files/SYLLABUS/1.B.Tech/1.R18/1.B.Tech I Year R18 Syllabus/R18B.Tech.ECE,ETE,EIE,ECM,ICE,CSE(AIML),CSE(IoT),CSE(DS),IT,CSIT,Syllabus.pdf"
                },
                "common_non_circuit": {
                    "name": "Common (Non-Circuit Branches including Automation, Robotics and Textile Engineering)",
                    "url": "https://studentservices.jntuh.ac.in/oss/resources/files/SYLLABUS/1.B.Tech/1.R18/1.B.Tech I Year R18 Syllabus/R18B.TechIYearSyllabusforNon_CircuitBranchesIncludingAutomationRoboticsandTextileEngineering.pdf"
                }
            },
            "2": {
                "aeronautical": {
                    "name": "Aeronautical Engineering",
                    "url": "https://studentservices.jntuh.ac.in/oss/resources/files/SYLLABUS/1.B.Tech/1.R18/2.B.Tech II Year R18 Syllabus/R-18 B.Tech AERONAUTICAL ENGG. II Year Syllabus.pdf"
                },
                "civil": {
                    "name": "Civil Engineering",
                    "url": "https://studentservices.jntuh.ac.in/oss/resources/files/SYLLABUS/1.B.Tech/1.R18/2.B.Tech II Year R18 Syllabus/R-18 B.Tech CIVIL ENGG. II Year Syllabus.pdf"
                },
                "cse": {
                    "name": "Computer Science and Engineering",
                    "url": "https://studentservices.jntuh.ac.in/oss/resources/files/SYLLABUS/1.B.Tech/1.R18/2.B.Tech II Year R18 Syllabus/R-18 B.Tech CSE II Year Syllabus.pdf"
                },
                "cse_cs": {
                    "name": "CSE (Cyber Security)",
                    "url": "https://studentservices.jntuh.ac.in/oss/resources/files/SYLLABUS/1.B.Tech/1.R18/2.B.Tech II Year R18 Syllabus/R-18 B.Tech CSE (Cyber Security) II Year Syllabus.pdf"
                },
                "cse_ds": {
                    "name": "CSE (Data Science)",
                    "url": "https://studentservices.jntuh.ac.in/oss/resources/files/SYLLABUS/1.B.Tech/1.R18/2.B.Tech II Year R18 Syllabus/R-18 B.Tech CSE (Data Science) II Year Syllabus.pdf"
                },
                "cse_aiml": {
                    "name": "CSE (AI & ML)",
                    "url": "https://studentservices.jntuh.ac.in/oss/resources/files/SYLLABUS/1.B.Tech/1.R18/2.B.Tech II Year R18 Syllabus/R-18 B.Tech CSE(AI&ML) II Year Syllabus.pdf"
                },
                "cse_iot": {
                    "name": "CSE (IoT)",
                    "url": "https://studentservices.jntuh.ac.in/oss/resources/files/SYLLABUS/1.B.Tech/1.R18/2.B.Tech II Year R18 Syllabus/R-18 B.Tech CSE(IoT) II Year Syllabus.pdf"
                },
                "ece": {
                    "name": "Electronics and Communication Engineering",
                    "url": "https://studentservices.jntuh.ac.in/oss/resources/files/SYLLABUS/1.B.Tech/1.R18/2.B.Tech II Year R18 Syllabus/R-18 B.Tech ECE II Year Syllabus.pdf"
                },
                "ecm": {
                    "name": "Electronics and Computer Engineering",
                    "url": "https://studentservices.jntuh.ac.in/oss/resources/files/SYLLABUS/1.B.Tech/1.R18/2.B.Tech II Year R18 Syllabus/R-18 B.Tech ECM II Year Syllabus.pdf"
                },
                "eee": {
                    "name": "Electrical and Electronics Engineering",
                    "url": "https://studentservices.jntuh.ac.in/oss/resources/files/SYLLABUS/1.B.Tech/1.R18/2.B.Tech II Year R18 Syllabus/R-18 B.Tech EEE II Year Syllabus.pdf"
                },
                "eie": {
                    "name": "Electronics and Instrumentation Engineering",
                    "url": "https://studentservices.jntuh.ac.in/oss/resources/files/SYLLABUS/1.B.Tech/1.R18/2.B.Tech II Year R18 Syllabus/R-18 B.Tech EIE II Year Syllabus.pdf"
                },
                "ete": {
                    "name": "Electronics and Telematics Engineering",
                    "url": "https://studentservices.jntuh.ac.in/oss/resources/files/SYLLABUS/1.B.Tech/1.R18/2.B.Tech II Year R18 Syllabus/R-18 B.Tech ETE II Year Syllabus.pdf"
                },
                "it": {
                    "name": "Information Technology",
                    "url": "https://studentservices.jntuh.ac.in/oss/resources/files/SYLLABUS/1.B.Tech/1.R18/2.B.Tech II Year R18 Syllabus/R-18 B.Tech IT II Year Syllabus.pdf"
                },
                "mech": {
                    "name": "Mechanical Engineering",
                    "url": "https://studentservices.jntuh.ac.in/oss/resources/files/SYLLABUS/1.B.Tech/1.R18/2.B.Tech II Year R18 Syllabus/R-18 B.Tech MECH II Year Syllabus.pdf"
                },
                "mechatronics": {
                    "name": "Mechatronics Engineering",
                    "url": "https://studentservices.jntuh.ac.in/oss/resources/files/SYLLABUS/1.B.Tech/1.R18/2.B.Tech II Year R18 Syllabus/R-18 B.Tech MECHATRONICS II Year Syllabus.pdf"
                },
                "mining": {
                    "name": "Mining Engineering",
                    "url": "https://studentservices.jntuh.ac.in/oss/resources/files/SYLLABUS/1.B.Tech/1.R18/2.B.Tech II Year R18 Syllabus/R-18 B.Tech MINING II Year Syllabus.pdf"
                },
                "mme": {
                    "name": "Metallurgical and Materials Engineering",
                    "url": "https://studentservices.jntuh.ac.in/oss/resources/files/SYLLABUS/1.B.Tech/1.R18/2.B.Tech II Year R18 Syllabus/R-18 B.Tech MME II Year Syllabus.pdf"
                },
                "petroleum": {
                    "name": "Petroleum Engineering",
                    "url": "https://studentservices.jntuh.ac.in/oss/resources/files/SYLLABUS/1.B.Tech/1.R18/2.B.Tech II Year R18 Syllabus/R-18 B.Tech PETROLEUM ENGG II Year Syllabus.pdf"
                }
            },
            "3": {
                "aeronautical": {
                    "name": "Aeronautical Engineering",
                    "url": "https://studentservices.jntuh.ac.in/oss/resources/files/SYLLABUS/1.B.Tech/1.R18/3.B.Tech III Year R18 Syllabus/R-18 B.Tech AERONAUTICAL ENGG. III Year Syllabus.pdf"
                },
                "civil": {
                    "name": "Civil Engineering",
                    "url": "https://studentservices.jntuh.ac.in/oss/resources/files/SYLLABUS/1.B.Tech/1.R18/3.B.Tech III Year R18 Syllabus/R-18 B.Tech CIVIL ENGG. III Year Syllabus.pdf"
                },
                "cse": {
                    "name": "Computer Science and Engineering",
                    "url": "https://studentservices.jntuh.ac.in/oss/resources/files/SYLLABUS/1.B.Tech/1.R18/3.B.Tech III Year R18 Syllabus/R-18 B.Tech CSE III Year Syllabus.pdf"
                },
                "cse_cs": {
                    "name": "CSE (Cyber Security)",
                    "url": "https://studentservices.jntuh.ac.in/oss/resources/files/SYLLABUS/1.B.Tech/1.R18/3.B.Tech III Year R18 Syllabus/R-18 B.Tech CSE (Cyber Security) III Year Syllabus.pdf"
                },
                "cse_ds": {
                    "name": "CSE (Data Science)",
                    "url": "https://studentservices.jntuh.ac.in/oss/resources/files/SYLLABUS/1.B.Tech/1.R18/3.B.Tech III Year R18 Syllabus/R-18 B.Tech CSE (Data Science) III Year Syllabus.pdf"
                },
                "cse_aiml": {
                    "name": "CSE (AI & ML)",
                    "url": "https://studentservices.jntuh.ac.in/oss/resources/files/SYLLABUS/1.B.Tech/1.R18/3.B.Tech III Year R18 Syllabus/R-18 B.Tech CSE(AI&ML) III Year Syllabus.pdf"
                },
                "cse_iot": {
                    "name": "CSE (IoT)",
                    "url": "https://studentservices.jntuh.ac.in/oss/resources/files/SYLLABUS/1.B.Tech/1.R18/3.B.Tech III Year R18 Syllabus/R-18 B.Tech CSE(IoT) III Year Syllabus.pdf"
                },
                "ece": {
                    "name": "Electronics and Communication Engineering",
                    "url": "https://studentservices.jntuh.ac.in/oss/resources/files/SYLLABUS/1.B.Tech/1.R18/3.B.Tech III Year R18 Syllabus/R-18 B.Tech ECE III Year Syllabus.pdf"
                },
                "ecm": {
                    "name": "Electronics and Computer Engineering",
                    "url": "https://studentservices.jntuh.ac.in/oss/resources/files/SYLLABUS/1.B.Tech/1.R18/3.B.Tech III Year R18 Syllabus/R-18 B.Tech ECM III Year Syllabus.pdf"
                },
                "eee": {
                    "name": "Electrical and Electronics Engineering",
                    "url": "https://studentservices.jntuh.ac.in/oss/resources/files/SYLLABUS/1.B.Tech/1.R18/3.B.Tech III Year R18 Syllabus/R-18 B.Tech EEE III Year Syllabus.pdf"
                },
                "eie": {
                    "name": "Electronics and Instrumentation Engineering",
                    "url": "https://studentservices.jntuh.ac.in/oss/resources/files/SYLLABUS/1.B.Tech/1.R18/3.B.Tech III Year R18 Syllabus/R-18 B.Tech EIE III Year Syllabus.pdf"
                },
                "ete": {
                    "name": "Electronics and Telematics Engineering",
                    "url": "https://studentservices.jntuh.ac.in/oss/resources/files/SYLLABUS/1.B.Tech/1.R18/3.B.Tech III Year R18 Syllabus/R-18 B.Tech ETE III Year Syllabus.pdf"
                },
                "it": {
                    "name": "Information Technology",
                    "url": "https://studentservices.jntuh.ac.in/oss/resources/files/SYLLABUS/1.B.Tech/1.R18/3.B.Tech III Year R18 Syllabus/R-18 B.Tech IT III Year Syllabus.pdf"
                },
                "mech": {
                    "name": "Mechanical Engineering",
                    "url": "https://studentservices.jntuh.ac.in/oss/resources/files/SYLLABUS/1.B.Tech/1.R18/3.B.Tech III Year R18 Syllabus/R-18 B.Tech MECH III Year Syllabus.pdf"
                },
                "mechatronics": {
                    "name": "Mechatronics Engineering",
                    "url": "https://studentservices.jntuh.ac.in/oss/resources/files/SYLLABUS/1.B.Tech/1.R18/3.B.Tech III Year R18 Syllabus/R-18 B.Tech MECHATRONICS III Year Syllabus.pdf"
                },
                "mining": {
                    "name": "Mining Engineering",
                    "url": "https://studentservices.jntuh.ac.in/oss/resources/files/SYLLABUS/1.B.Tech/1.R18/3.B.Tech III Year R18 Syllabus/R-18 B.Tech MINING III Year Syllabus.pdf"
                },
                "mme": {
                    "name": "Metallurgical and Materials Engineering",
                    "url": "https://studentservices.jntuh.ac.in/oss/resources/files/SYLLABUS/1.B.Tech/1.R18/3.B.Tech III Year R18 Syllabus/R-18 B.Tech MME III Year Syllabus.pdf"
                },
                "petroleum": {
                    "name": "Petroleum Engineering",
                    "url": "https://studentservices.jntuh.ac.in/oss/resources/files/SYLLABUS/1.B.Tech/1.R18/3.B.Tech III Year R18 Syllabus/R-18 B.Tech PETROLEUM ENGG III Year Syllabus.pdf"
                },
                "open_electives": {
                    "name": "Open Electives",
                    "url": "https://studentservices.jntuh.ac.in/oss/resources/files/SYLLABUS/1.B.Tech/1.R18/3.B.Tech III Year R18 Syllabus/R-18 B.Tech OpenElectives III Year Syllabus.pdf"
                }
            },
            "4": {
                "aeronautical": {
                    "name": "Aeronautical Engineering",
                    "url": "https://studentservices.jntuh.ac.in/oss/resources/files/SYLLABUS/1.B.Tech/1.R18/4.B.Tech IV Year R18 Syllabus/R-18 B.Tech AE IV Year Syllabus.pdf"
                },
                "civil": {
                    "name": "Civil Engineering",
                    "url": "https://studentservices.jntuh.ac.in/oss/resources/files/SYLLABUS/1.B.Tech/1.R18/4.B.Tech IV Year R18 Syllabus/R-18 B.Tech CIVIL IV Year Syllabus.pdf"
                },
                "cse": {
                    "name": "Computer Science and Engineering",
                    "url": "https://studentservices.jntuh.ac.in/oss/resources/files/SYLLABUS/1.B.Tech/1.R18/4.B.Tech IV Year R18 Syllabus/R-18 B.Tech CSE IV Year Syllabus.pdf"
                },
                "cse_cs": {
                    "name": "CSE (Cyber Security)",
                    "url": "https://studentservices.jntuh.ac.in/oss/resources/files/SYLLABUS/1.B.Tech/1.R18/4.B.Tech IV Year R18 Syllabus/R-18 B.Tech CSE (Cyber Security) IV Year Syllabus.pdf"
                },
                "cse_ds": {
                    "name": "CSE (Data Science)",
                    "url": "https://studentservices.jntuh.ac.in/oss/resources/files/SYLLABUS/1.B.Tech/1.R18/4.B.Tech IV Year R18 Syllabus/R-18 B.Tech CSE (Data Science) IV Year Syllabus.pdf"
                },
                "cse_aiml": {
                    "name": "CSE (AI & ML)",
                    "url": "https://studentservices.jntuh.ac.in/oss/resources/files/SYLLABUS/1.B.Tech/1.R18/4.B.Tech IV Year R18 Syllabus/R-18 B.Tech CSE(AI&ML) IV Year Syllabus.pdf"
                },
                "cse_iot": {
                    "name": "CSE (IoT)",
                    "url": "https://studentservices.jntuh.ac.in/oss/resources/files/SYLLABUS/1.B.Tech/1.R18/4.B.Tech IV Year R18 Syllabus/R-18 B.Tech CSE(IoT) IV Year Syllabus.pdf"
                },
                "ece": {
                    "name": "Electronics and Communication Engineering",
                    "url": "https://studentservices.jntuh.ac.in/oss/resources/files/SYLLABUS/1.B.Tech/1.R18/4.B.Tech IV Year R18 Syllabus/R-18 B.Tech ECE IV Year Syllabus.pdf"
                },
                "ecm": {
                    "name": "Electronics and Computer Engineering",
                    "url": "https://studentservices.jntuh.ac.in/oss/resources/files/SYLLABUS/1.B.Tech/1.R18/4.B.Tech IV Year R18 Syllabus/R-18 B.Tech ECM IV Year Syllabus.pdf"
                },
                "eee": {
                    "name": "Electrical and Electronics Engineering",
                    "url": "https://studentservices.jntuh.ac.in/oss/resources/files/SYLLABUS/1.B.Tech/1.R18/4.B.Tech IV Year R18 Syllabus/R-18 B.Tech EEE IV Year Syllabus.pdf"
                },
                "eie": {
                    "name": "Electronics and Instrumentation Engineering",
                    "url": "https://studentservices.jntuh.ac.in/oss/resources/files/SYLLABUS/1.B.Tech/1.R18/4.B.Tech IV Year R18 Syllabus/R-18 B.Tech EIE IV Year Syllabus.pdf"
                },
                "ete": {
                    "name": "Electronics and Telematics Engineering",
                    "url": "https://studentservices.jntuh.ac.in/oss/resources/files/SYLLABUS/1.B.Tech/1.R18/4.B.Tech IV Year R18 Syllabus/R-18 B.Tech ETE IV Year Syllabus.pdf"
                },
                "it": {
                    "name": "Information Technology",
                    "url": "https://studentservices.jntuh.ac.in/oss/resources/files/SYLLABUS/1.B.Tech/1.R18/4.B.Tech IV Year R18 Syllabus/R-18 B.Tech IT IV Year Syllabus.pdf"
                },
                "mech": {
                    "name": "Mechanical Engineering",
                    "url": "https://studentservices.jntuh.ac.in/oss/resources/files/SYLLABUS/1.B.Tech/1.R18/4.B.Tech IV Year R18 Syllabus/R-18 B.Tech MECH IV Year Syllabus.pdf"
                },
                "mechatronics": {
                    "name": "Mechatronics Engineering",
                    "url": "https://studentservices.jntuh.ac.in/oss/resources/files/SYLLABUS/1.B.Tech/1.R18/4.B.Tech IV Year R18 Syllabus/R-18 B.Tech MECHATRONICS IV Year Syllabus.pdf"
                },
                "mining": {
                    "name": "Mining Engineering",
                    "url": "https://studentservices.jntuh.ac.in/oss/resources/files/SYLLABUS/1.B.Tech/1.R18/4.B.Tech IV Year R18 Syllabus/R-18 B.Tech MINING IV Year Syllabus.pdf"
                },
                "mme": {
                    "name": "Metallurgical and Materials Engineering",
                    "url": "https://studentservices.jntuh.ac.in/oss/resources/files/SYLLABUS/1.B.Tech/1.R18/4.B.Tech IV Year R18 Syllabus/R-18 B.Tech MME IV Year Syllabus.pdf"
                },
                "petroleum": {
                    "name": "Petroleum Engineering",
                    "url": "https://studentservices.jntuh.ac.in/oss/resources/files/SYLLABUS/1.B.Tech/1.R18/4.B.Tech IV Year R18 Syllabus/R-18 B.Tech PETROLEUM ENGG IV Year Syllabus.pdf"
                },
                "textile": {
                    "name": "Textile Engineering",
                    "url": "https://studentservices.jntuh.ac.in/oss/resources/files/SYLLABUS/1.B.Tech/1.R18/4.B.Tech IV Year R18 Syllabus/R-18 B.Tech TEXTILE IV Year Syllabus.pdf"
                },
                "open_electives": {
                    "name": "Open Electives",
                    "url": "https://studentservices.jntuh.ac.in/oss/resources/files/SYLLABUS/1.B.Tech/1.R18/4.B.Tech IV Year R18 Syllabus/R-18B.Tech OpenElective IV Year Syllabus.pdf"
                }
            }
        }
    },
    "bpharmacy": {
        "r22": {
            "1": {
                "common": {
                    "name": "B.Pharmacy I Year",
                    "url": "https://studentservices.jntuh.ac.in/oss/resources/files/SYLLABUS/2.B.Pharmacy/8.R22/1.B.Pharmacy I Year Syllabus/R22 B.Pharmacy I Year Syllabus.pdf"
                }
            },
            "2": {
                "common": {
                    "name": "B.Pharmacy II Year",
                    "url": "https://studentservices.jntuh.ac.in/oss/resources/files/SYLLABUS/2.B.Pharmacy/8.R22/2.B.Pharmacy II Year Syllabus/R22 B.Pharmacy II Year Syllabus.pdf"
                }
            }
        }
    },
    "mba": {
        "r22": {
            "1": {
                "common": {
                    "name": "MBA (Years I & II)",
                    "url": "https://studentservices.jntuh.ac.in/oss/resources/files/SYLLABUS/5.MBA/1.R22/R22 MBA Syllabus.pdf"
                }
            }
        }
    },
    "mca": {
        "r22": {
            "1": {
                "common": {
                    "name": "MCA (Years I & II)",
                    "url": "https://studentservices.jntuh.ac.in/oss/resources/files/SYLLABUS/6.MCA/1.R22/R22 MCA Syllabus.pdf"
                }
            }
        }
    },
    "mpharmacy": {
        "r22": {
            "1": {
                "industrial_pharmacy": {
                    "name": "M.Pharm - Industrial Pharmacy",
                    "url": "https://studentservices.jntuh.ac.in/oss/resources/files/SYLLABUS/4.M.Pharmacy/1.R22 Syllabus/R22 M.Pharm. Industrial Pharmacy Syllabus.pdf"
                },
                "pharmaceutical_analysis": {
                    "name": "M.Pharm - Pharmaceutical Analysis",
                    "url": "https://studentservices.jntuh.ac.in/oss/resources/files/SYLLABUS/4.M.Pharmacy/1.R22 Syllabus/R22 M.Pharm. Pharmaceutical Analysis Syllabus.pdf"
                },
                "pharmaceutical_chemistry": {
                    "name": "M.Pharm - Pharmaceutical Chemistry",
                    "url": "https://studentservices.jntuh.ac.in/oss/resources/files/SYLLABUS/4.M.Pharmacy/1.R22 Syllabus/R22 M.Pharm. Pharmaceutical Chemistry Syllabus.pdf"
                },
                "pharmaceutical_qa": {
                    "name": "M.Pharm - Pharmaceutical Quality Assurance",
                    "url": "https://studentservices.jntuh.ac.in/oss/resources/files/SYLLABUS/4.M.Pharmacy/1.R22 Syllabus/R22 M.Pharm. Pharmaceutical Quality Assurance Syllabus.pdf"
                },
                "pharmaceutical_regulatory": {
                    "name": "M.Pharm - Pharmaceutical Regulatory Affairs",
                    "url": "https://studentservices.jntuh.ac.in/oss/resources/files/SYLLABUS/4.M.Pharmacy/1.R22 Syllabus/R22 M.Pharm. Pharmaceutical Regulatory Affairs.pdf"
                },
                "pharmaceutics_tech": {
                    "name": "M.Pharm - Pharmaceutics (Pharmaceutical Technology)",
                    "url": "https://studentservices.jntuh.ac.in/oss/resources/files/SYLLABUS/4.M.Pharmacy/1.R22 Syllabus/R22 M.Pharm. Pharmaceutics - Pharmaceutical Technology Syllabus.pdf"
                },
                "pharmacognosy": {
                    "name": "M.Pharm - Pharmacognosy",
                    "url": "https://studentservices.jntuh.ac.in/oss/resources/files/SYLLABUS/4.M.Pharmacy/1.R22 Syllabus/R22 M.Pharm. Pharmacognosy.pdf"
                },
                "pharmacology": {
                    "name": "M.Pharm - Pharmacology",
                    "url": "https://studentservices.jntuh.ac.in/oss/resources/files/SYLLABUS/4.M.Pharmacy/1.R22 Syllabus/R22 M.Pharm. Pharmacology Syllabus.pdf"
                },
                "pharmacy_practice": {
                    "name": "M.Pharm - Pharmacy Practice",
                    "url": "https://studentservices.jntuh.ac.in/oss/resources/files/SYLLABUS/4.M.Pharmacy/1.R22 Syllabus/R22 M.Pharm. Pharmacy Practice Syllabus.pdf"
                }
            }
        }
    }
}


class JNTUHSyllabusClient:
    """Client for fetching JNTUH syllabus data with direct PDF links."""
    
    def get_branches(self, degree: str, regulation: str, year: str) -> Dict:
        """
        Get available branches for a given degree, regulation, and year.
        """
        degree = degree.lower()
        regulation = regulation.lower()
        
        # Check if degree exists
        if degree not in SYLLABUS_PDF_MAP:
            return {'error': f'Degree "{degree}" not found'}
        
        # Check if regulation exists
        if regulation not in SYLLABUS_PDF_MAP[degree]:
            return {'error': f'Regulation "{regulation}" not found for {degree}'}
        
        # Check if year exists
        if year not in SYLLABUS_PDF_MAP[degree][regulation]:
            return {'error': f'Year {year} not available yet. JNTUH has not uploaded PDFs for this year.'}
        
        branches = []
        for branch_code, branch_data in SYLLABUS_PDF_MAP[degree][regulation][year].items():
            branches.append({
                'code': branch_code,
                'name': branch_data['name']
            })
        
        return {'success': True, 'branches': branches}
    
    def get_syllabus_pdf(self, degree: str, regulation: str, year: str, branch: str) -> Dict:
        """
        Get direct PDF URL for a specific degree, regulation, year, and branch.
        """
        degree = degree.lower()
        regulation = regulation.lower()
        branch = branch.lower()
        
        # Check if degree exists
        if degree not in SYLLABUS_PDF_MAP:
            return {'error': f'Degree "{degree}" not found'}
        
        # Check if regulation exists
        if regulation not in SYLLABUS_PDF_MAP[degree]:
            return {'error': f'Regulation "{regulation}" not found for {degree}'}
        
        # Check if year exists
        if year not in SYLLABUS_PDF_MAP[degree][regulation]:
            return {'error': f'Year {year} not available yet'}
        
        # Check if branch exists
        if branch not in SYLLABUS_PDF_MAP[degree][regulation][year]:
            return {'error': f'Branch "{branch}" not found for {degree} {regulation} Year {year}'}
        
        pdf_data = SYLLABUS_PDF_MAP[degree][regulation][year][branch]
        
        return {
            'success': True,
            'pdf': {
                'name': pdf_data['name'],
                'url': pdf_data['url']
            }
        }
