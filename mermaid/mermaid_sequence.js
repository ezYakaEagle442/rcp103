const fs = require('fs');
const path = require('path');

/**
 ***************************************************************
* mermaid_sequence.js
 *
 * usage :
 * node ./mermaid/mermaid_sequence.js
 * mmdc --version
 * mmdc -i ./mermaid/mermaid_sequence.mmd -o ./mermaid/mermaid_sequence.png
 * mmdc -i ./mermaid/mermaid_sequence.mmd -o ./mermaid/mermaid_sequence.svg
 * start ./mermaid/mermaid_sequence.svg
 * 
 ***************************************************************

 * Génère un diagramme Mermaid à partir du modèle fourni.
 * Écrit le diagramme dans mermaid_xxx.mmd et l'affiche sur la console.
 *
 * Utilisation:
 *   cd C:\github\rcp103
 *   sudo apt upgrade nodejs
 *   node --version
 *   printenv
*/

const mermaid = `%%{init: {"theme":"default"}}%%
sequenceDiagram
    participant Engine
    participant GatewayImpl
    participant ClientImpl
    participant SchedulerImpl
    participant QueueImpl
    participant ServerImpl
    participant EventImpl
    participant MessageImpl

    Engine->>Engine: main()
    Engine->>SchedulerImpl: instantiate
    Engine->>Engine: create_gateway()
    Engine->>GatewayImpl: create_servers()
    GatewayImpl->>ServerImpl: Server.append()
    GatewayImpl->>GatewayImpl: listen()
    Engine->>Engine: run_simulationMM1()
    ServerImpl->>QueueImpl: is_empty()
    ServerImpl->>QueueImpl: dequeue()
    Engine->>ClientImpl: create_clients()
    ClientImpl->>SchedulerImpl: analyze events
    ClientImpl->>GatewayImpl: send_message(msg)
    GatewayImpl->>QueueImpl: enqueue(msg)
    QueueImpl->>QueueImpl: count_messages()
    QueueImpl->>QueueImpl: queue.append(msg)
    QueueImpl->>QueueImpl: is_empty()
    QueueImpl->>QueueImpl: popleft()
    Engine->>Engine: run_tests()
    Engine->>SchedulerImpl: get_event()
    Engine->>Engine: print_metrics()

    `;

const outFile = path.join(__dirname, 'mermaid_sequence.mmd');

try {
    // console.log('CACHE_PATH:', CACHE_PATH);

    fs.writeFileSync(outFile, mermaid, { encoding: 'utf8' });
    console.log('Mermaid diagram generated:', outFile);
    console.log('--- Diagram preview ---');
    console.log(mermaid);
} catch (err) {
    console.error('Erreur lors de l\'écriture du fichier Mermaid:', err);
    process.exit(1);
}