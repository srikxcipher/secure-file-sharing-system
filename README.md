# Secure File Sharing System using DES and Diffie Hellman Algorithm.

---
<!--
<img src="https://github.com/srikxcipher/secure-file-sharing-system/blob/5cdc75a3bcfda05324334c690c14fda463595871/docs/pro-diagram.png" alt="System Diagram" style="float: right; width: 300px;">
-->



<h3>System Diagram</h3>
<!-- System Overview Section -->
<table>
  <tr>
    <td style="width: 50%; vertical-align: top;">
      <img src="https://github.com/srikxcipher/secure-file-sharing-system/blob/5cdc75a3bcfda05324334c690c14fda463595871/docs/pro-diagram.png" alt="System Diagram" width="80%">
    </td>
    <td style="width: 50%; vertical-align: top;">
      <h3>File Encryption Process</h3>
      <ol>
        <li>User selects a file using the <strong>"Send File"</strong> button.</li>
        <li>File is read as binary data.</li>
        <li>Diffie-Hellman key exchange is performed to securely exchange the key.</li>
        <li>File data is padded and encrypted using the <strong>DES algorithm</strong>.</li>
        <li>Encrypted data is sent to the server along with a <strong>SHA-256 hash</strong> for integrity verification.</li>
      </ol>
      <h3>File Decryption (Server-Side)</h3>
      <ol>
        <li>Server receives the encrypted file.</li>
        <li>Performs the same Diffie-Hellman key exchange to derive the shared key.</li>
        <li>Uses the shared key to decrypt the file via DES.</li>
        <li>Verifies file integrity using the provided SHA-256 hash.</li>
        <li>Decrypted file is saved or processed as needed.</li>
      </ol>
      <h3>System Workflow</h3>
      <ol>
        <li><strong>Client:</strong>
          <ul>
            <li>Selects a file using the GUI.</li>
            <li>Performs key exchange (Diffie-Hellman).</li>
            <li>Encrypts file using DES.</li>
            <li>Sends encrypted file and hash to server.</li>
          </ul>
        </li>
        <li><strong>Server:</strong>
          <ul>
            <li>Receives the encrypted file.</li>
            <li>Repeats key exchange.</li>
            <li>Decrypts using DES.</li>
            <li>Verifies integrity with SHA-256.</li>
          </ul>
        </li>
      </ol>
      <h3>Quick Legend</h3>
      <ul>
        <li><strong>DH</strong>: Diffie-Hellman (key exchange)</li>
        <li><strong>DES</strong>: Data Encryption Standard</li>
        <li><strong>SHA-256</strong>: Secure Hash Algorithm (integrity check)</li>
        <li><span style="color:blue;">Client Side</span>: handles encryption and hashing</li>
        <li><span style="color:green;">Server Side</span>: handles decryption and verification</li>
      </ul>
    </td>
  </tr>
</table>

  ---

  ### Snapshots
  <img src="https://github.com/srikxcipher/secure-file-sharing-system/blob/33a7419d0484d877f0055eb8d9047f58113aa7c1/docs/output-doc-page-001.jpg" width="100%">

---

  
<table>
  <tr>
    <td style="width: 50%; vertical-align: top;">
        <h2> Sender ➡️</h2>
       <img src="https://github.com/srikxcipher/secure-file-sharing-system/blob/33a7419d0484d877f0055eb8d9047f58113aa7c1/docs/output-doc-page-003.jpg" width="100%">
    </td>
    <td style="width: 50%; vertical-align: top;">
        <h2> Receiver ➡️</h2>
        <img src="https://github.com/srikxcipher/secure-file-sharing-system/blob/33a7419d0484d877f0055eb8d9047f58113aa7c1/docs/output-doc-page-002.jpg" width="100%">
    </td>
  </tr>
</table>

