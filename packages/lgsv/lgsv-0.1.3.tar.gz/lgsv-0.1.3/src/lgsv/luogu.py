"""
luogu class
"""

import asyncio
import json

import httpx

headers = {
    "Accept": "application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
    "Referer": "https://www.luogu.com.cn/",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "cross-site",
    "Priority": "u=0, i",
    "x-lentille-request": "content-only",
}
params = {"_contentOnly": ""}

"""
async def fetch_csrf_token():
    获取csrf token
    async with httpx.AsyncClient() as client:
        response = await client.get(
            url="https://www.luogu.com.cn",
            #            params=params,
            headers=headers,
#            cookies=cookies,
        )
    soup = BeautifulSoup(response.text, "html.parser")
    csrf_token = soup.find("meta", attrs={"name": "csrf-token"})
    headers["x-csrf-token"] = csrf_token.get("content")
    return headers["x-csrf-token"]
"""


class HttpError(Exception):
    """
    HTTP 异常。
    由于处理各类 HTTP 错误。
    """

    def __init__(self, msg):
        self.message = msg


class Problem:
    """洛谷题目类"""

    __BASE_URL = "https://www.luogu.com.cn/problem/"
    problem_id: str
    # data = None
    markdown: str
    difficulty: int
    tags: list
    limits = {"time": [], "memory": []}
    content: dict
    accepted: bool
    submitted: bool
    sample: list

    def __init__(self, problem_id) -> None:
        self.problem_id = problem_id

    def part_markdown(self, part):
        """单独获取题目的部分markdown,如题目背景,题目描述等"""
        ret = None
        p = part
        match part:
            case "samples" | "s":
                ret = "## 输入输出样例"
                p = "samples"
            case "background" | "b":
                ret = "## 题目背景"
                p = "background"
            case "formatI" | "if":
                ret = "## 输入格式"
                p = "formatI"
            case "formatO" | "of":
                ret = "## 输出格式"
                p = "formatO"
            case "hint" | "h":
                ret = "## 说明/提示"
                p = "hint"
            case "name" | "n":
                ret = "# "
                p = "name"
            case "description" | "d":
                ret = "## 题目描述"
                p = "description"
            case "translation" | "tr":
                ret = "## 题目翻译"
                p = "translation"
        if p != "name":
            ret += "\n"
        if p == "samples":
            for i, sample in enumerate(self.sample):
                ret += (
                    f"### 输入 \\#{str(i+1)}\n"
                    f"```\n"
                    f"{sample[0]}\n"
                    f"```\n"
                    f"### 输出 \\#{str(i+1)}\n"
                    f"```\n"
                    f"{sample[1]}\n"
                    f"```\n"
                )
            return ret
        if p not in self.content or self.content[p] is None or self.content[p]=="":
            return ""
        return ret + self.content[p] + "\n"

    async def fetch_resources(self):
        """取回题目资源并将其存储到 self.data 中,返回 self.data"""
        # 将请求存储到 __html_cache 中
        print("从" + self.__BASE_URL + self.problem_id + "获取数据")
        async with httpx.AsyncClient() as client:
            raw_resources = await client.get(
                self.__BASE_URL + self.problem_id,
                params=params,
                headers=headers,
                follow_redirects=True,
            )
        print("解析题目" + self.problem_id)
        # 解析请求到的 json
        rescoures = json.loads(raw_resources.text)
        if rescoures["status"] != 200:
            raise HttpError(
                f"访问{self.__BASE_URL}{self.problem_id}失败：HTTP ERROR {rescoures['code']}"
            )
        data = rescoures["data"]["problem"]
        self.difficulty = data["difficulty"]
        self.tags = data["tags"]
        self.limits = data["limits"]
        self.content = data["content"]
        self.sample = data["samples"]
        if "accepted" in data:
            self.accepted = data["accepted"]
        else:
            self.accepted = False
        if "submmited" in data:
            self.submitted = data["submmited"]
        else:
            self.submitted = False
        return data

    def get_markdown(self, order=None):
        """以 order 的顺序获取题目的markdown"""
        if hasattr(self, "markdown"):
            return self.markdown
        self.markdown = self.part_markdown("name")
        for c in order:
            self.markdown += self.part_markdown(c)
        cnt_d = 0
        i = 0
        while i < len(self.markdown):
            if self.markdown[i] == "$":
                cnt_d += 1

                if (cnt_d & 1) == 1:
                    if self.markdown[i + 1] == "$":
                        i += 1
                    nxt_c = i + 1
                    while self.markdown[nxt_c] == " ":
                        nxt_c += 1
                    self.markdown = (
                        self.markdown[: i + 1]
                        + self.markdown[-(len(self.markdown) - nxt_c) :]
                    )
                else:
                    prev_c = i - 1
                    while self.markdown[prev_c] == " ":
                        prev_c -= 1
                    self.markdown = (
                        self.markdown[: prev_c + 1]
                        + self.markdown[-(len(self.markdown) - i) :]
                    )
                    i = prev_c + 1
                    if self.markdown[i + 1] == "$":
                        i += 1
            i += 1
        return self.markdown


class Training:
    """洛谷题单类"""

    __BASE_URL = "https://www.luogu.com.cn/training/"
    training_id = ""
    problem_list = []
    markdown: str

    def __init__(self, training_id) -> None:
        self.training_id = training_id

    async def fetch_resources(self):
        """取回题目资源并将其存储到 self.data 中,返回 self.data"""
        print("从" + self.__BASE_URL + self.training_id + "获取数据")
        async with httpx.AsyncClient() as client:
            raw_resources = await client.get(
                self.__BASE_URL + self.training_id,
                params=params,
                headers=headers,
                follow_redirects=True,
            )
        print("解析题单" + self.training_id)
        rescoures = json.loads(raw_resources.text)
        if rescoures["code"] != 200:
            raise HttpError(
                f"访问{self.__BASE_URL}{self.training_id}失败：HTTP ERROR {rescoures['code']}"
            )
        data = rescoures["currentData"]["training"]
        for p in data["problems"]:
            self.problem_list.append(Problem(problem_id=p["problem"]["pid"]))
        async with asyncio.TaskGroup() as tg:
            for p in self.problem_list:
                tg.create_task(p.fetch_resources())
        return data

    def get_markdown(self, order: list):
        """获取题单中所有题目的 markdown"""
        self.markdown = ""
        for p in self.problem_list:
            self.markdown += p.get_markdown(order)
        return self.markdown


class ProblemFilter:
    """filter of problems"""

    def __init__(self):
        pass

    def __call__(self, p: Problem) -> bool:
        pass
