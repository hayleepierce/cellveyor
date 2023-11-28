# cellveyor

## Example Command

```
poetry run cellveyor --spreadsheet-directory \
/home/gkapfham/working/data/gradebook/2023 --spreadsheet-file CMPSC-203-Fall-2023-Gradebook.xlsx \
--sheet-name Main \
--key-attribute "Student GitHub" \
--key-value "gkapfham" \
--column-regexp "^(Summary Grade|Final Grade) .*$" \
--feedback-regexp "Summary Grade 1 - Feedback" \
--feedback-file /home/gkapfham/working/teaching/github-classroom/feedback/all/feedback.yml \
--feedback-file /home/gkapfham/working/teaching/github-classroom/feedback/developer-development/feedback-overall-course-assessment.yml \
--github-token <Private GitHub Acess Token> \
--github-organization Allegheny-Computer-Science-203-F2023 \
--github-repository-prefix computer-science-203-fall-2023-course-assessment \
--transfer-report
```

🎉 Introduction

- Cellveyor is a python program that produces assignment reports for students or classes. Using cellveyor will
publicly give grade reports including feedback for created assignments. Using the cellveyor tool will quickly
run and send reports to members included in a locally created google spreadsheet. By running the command created,
this will quickly and automatically send out these reports in a very timely and efficient fashion.


 😂 Definitions


 🔋Features


 ⚡️ Requirements
- Cellveyor git hub repository
- Local google sheet
- Git hub token

 🔽 Installation
Follow these steps to install the cellveyor program:
1. Copy the ssh key of the repo
2. ```Git clone``` the repository onto your personal computer
- ```git clone (ssh key)``
3. type ```poetry run cellveyor --help``` to learn how to use the tool

 🪂 Configuration


 ✨ Analysis


 🚧 Integration


 🌄 Results


 🌎 Deployment



