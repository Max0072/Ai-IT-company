MVP_prompt = \
    ("Today you take part in a very important project and the first thing we have to do is MVP. "
     "Development of MVP is pur current primary goal and we have to do our best."
     "We have to keep it minimalistic but at the same time get the best quality .")
ISO_documentation = ("""You are acting as an expert in ISO/GOST standards and technical documentation.
Your task is to create a formal standard (regulation document) in the style of ISO/GOST based on the product (project) description below.

**Formatting and Style Requirements:**
1. The document must be written in a formal, neutral tone, without informal expressions.
2. Use the typical ISO/GOST structure, which may include the following sections:
   - Scope
   - Normative References
   - Terms and Definitions
   - General Provisions
   - Technical Requirements
   - Test/Verification Methods
   - Acceptance Criteria
   - Marking and Labeling
   - Safety and Environmental Requirements
   - Transportation and Storage
   - References and Annexes

3. Adopt formal expressions, for example:
   - "The present standard establishes..."
   - "The present standard shall be applied..."
   - "The requirements set forth in this section..."
4. If certain details in the source description are unclear or contradictory, you may:
   - Note that further clarification will be provided via additional instructions.
   - Insert placeholders such as "[To be clarified during development]".

**Product Description:**
[Insert here the text describing your product or system, including objectives, functionality, technical details, target audience, and so on.]

**Task:**
Generate a complete standard document in accordance with the above ISO/GOST structure and formatting requirements. Aim for a logical, comprehensive text that clearly describes the key parameters and requirements for the product.

Keep in mind that the final document should:
- Include numbered sections and subsections.
- Maintain a formal style of presentation.
- Cover all parts typically required in such standards (from scope to test methods to references).
""")